from flask import Flask, render_template, request, flash, jsonify, url_for, session, redirect, send_file
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import os

# Other modules
from operation_user_info import insert_data_into_operation_info
from client_user_info import insert_data_into_client_info
from uploadfiles import upload_filess
from login import send_data_for_login
from specific_user_files import fetch_particular_user_files
from fetch_all_files import fetch_all_files
from increase_download_count import download_count_increase
# Extra
import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()

app = Flask(__name__)

# Config file
app.config.from_pyfile('config.py')

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


mail = Mail(app)


s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Extra


@app.route("/")
def home():
    dbname = os.getenv("DB_NAME")
    user = os.getenv("UP_USER")
    password = os.getenv("PASSWORD")
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    return f"{dbname}\n,{user}\n,{password}\n,{host}\n,{port}"


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    result = send_data_for_login(data)
    return result


def send_verification_email(all_info):
    email = all_info['email']
    token = s.dumps(all_info, salt="verificaion")
    msg = Message('Confirm Email', recipients=[email])
    link = url_for('verify', token=token)
    msg.body = f'Your verification link is http://13.50.73.200:5000{link}'
    mail.send(msg)


@app.route("/api/registration", methods=['POST'])
def registration():
    data = request.json
    if data["type"] == "operation":
        result = insert_data_into_operation_info(data["info"])
    elif data["type"] == 'client':
        all_info = data["info"]
        # send verification email
        send_verification_email(all_info)

        result = {
            "message": "Verification link is sent to your Email"

        }
    else:
        result = {
            "message": "User type is not defined"

        }

    return jsonify(result)


@app.route("/verify/<token>", methods=["GET", "POST"])
def verify(token):
    try:
        all_info = s.loads(token, salt="verificaion", max_age=60)
        result = insert_data_into_client_info(all_info)
        return "You Are Successfully Registered"
    except SignatureExpired:
        return "Your token is expired"


@app.route("/api/upload", methods=["GET", "POST"])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    # if file.filename == '':
    #     return redirect(request.url)
    ouid = request.form.get('ouid')
    result = upload_filess(ouid, file, app)
    return result


@app.route("/api/get_files")
def get_files():
    ouid = request.args.get('ouid')
    result = fetch_particular_user_files(ouid)
    return result


@app.route('/api/get_all_files')
def get_all_files():
    result = fetch_all_files()
    return result


# @app.route("/api/download/<filename>", methods=["GET", "POST"])
# def download(filename):
#     # data = request.json
#     # location = data['location']
#     location = f"uploads/{filename}"
#     return send_file(location, as_attachment=True)

used_tokens = set()


def generate_secure_download_url(filename_cuid):
    # Generate a secure token for the filename
    # token = s.dumps({'filename_cuid': filename_cuid})
    token = s.dumps(filename_cuid)

    used_tokens.add(token)
    return f'/api/secure_download/{token}'


@app.route('/api/download', methods=['POST'])
def generate_download_url():
    filename_cuid = request.json
    download_url = generate_secure_download_url(filename_cuid)
    return jsonify({'download_url': download_url, 'cuid': filename_cuid['cuid']})


@app.route('/api/secure_download/<token>', methods=['GET', 'POST'])
def secure_download(token):
    try:
        # Verify and load the token
        data = s.loads(token)
        filename = data['filename']
        cuid = data['cuid']
        location = f"uploads/{filename}"
        # return f"{filename} {cuid}"
        # Check if the file exists before allowing the download
        post_data = request.json
        if os.path.exists(location):
            used_tokens.remove(token)
            if cuid == post_data['cuid']:
                # Increase download count
                download_count_increase(location)
                return send_file(location, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:

        return jsonify({'error': 'Invalid or expired token'}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
    # app.run(debug=True)
