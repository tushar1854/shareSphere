from flask import Flask, render_template, redirect, request, url_for, flash, session, jsonify, send_file
from flask_bootstrap import Bootstrap
import threading
import time
import requests
from io import BytesIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
Bootstrap(app)


# API call functions

# result1 = None
# result2 = None
# URL = "http://ec2-16-16-58-122.eu-north-1.compute.amazonaws.com"
# URL = "http://127.0.0.1:5000"
URL = "http://backend:5000"


# session['uid'] = False


def send_data_for_registration(form_data):
    url = f"{URL}/api/registration"
    response = requests.post(url, json=form_data)
    result = response.json()
    return result


def send_data_for_login(form_data):
    url = f"{URL}/api/login"
    response = requests.post(url, json=form_data)
    result = response.json()
    return result


def get_uploaded_files(ouid):
    url = f"{URL}/api/get_files"
    params = {
        "ouid": ouid
    }
    response = requests.get(url, params=params)
    result = response.json()
    return result


@app.route('/logout')
def logout():
    session.pop('ouid', None)
    session.pop('cuid', None)
    session.pop('type', None)
    return redirect(url_for('home'))


@app.route("/")
def home():
    if 'type' in session:
        if session['type'] == "operation":
            return redirect(url_for("uploads"))
        else:
            return redirect(url_for('generate_link'))

    return render_template("index.html", current_type=False)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form_data = {"type": request.form['user_type'].lower(),
                     "info": {
                         "firstname": request.form['first_name'],
            "lastname": request.form['last_name'],
            "email": request.form['email'],
            "password": request.form['pass']
        }
        }
        # Send data for registration
        send_data_for_registration(form_data)

        if request.form['user_type'].lower() == "client":
            flash("Verification Link is send to your Email")
        return redirect(url_for('login'))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form_data = {
            "email": request.form['email'],
            "password": request.form['pass']
        }
        result = send_data_for_login(form_data)
        if result['success'] == 0:
            flash("Incorrect Credentials, Try Again")
        elif result['success'] == 1:
            session['type'] = result['type']
            if session['type'] == "operation":
                session['ouid'] = result['uid']
                return redirect(url_for('uploads'))
            elif session['type'] == "client":
                session['cuid'] = result['uid']
                return redirect(url_for('generate_link'))

    return render_template("login.html")


def send_for_upload(file, ouid):
    url = f"{URL}/api/upload"
    print(ouid)
    response = requests.post(url, files=file, data=ouid)
    result = response.json()
    return result


@app.route("/upload", methods=["GET", "POST"])
def uploads():
    if request.method == "POST":
        uploaded_file = request.files['file']

        # print(f"saini{uploaded_file}")
        # print(ouid)
        file = {
            "file": (uploaded_file.filename, uploaded_file.stream, uploaded_file.mimetype)
        }
        ouid = {
            "ouid": session['ouid']
        }
        send_for_upload(file, ouid)
        return redirect(url_for('uploads'))

    if 'ouid' in session:
        ouid = session['ouid']
        if session['type'] != "operation":
            return "You Are Not An Operation User"
        else:
            filename = get_uploaded_files(ouid)
            return render_template("uploadfile.html", filename=filename, current_type=session['type'])
    else:
        return "You Need To Login First"


def get_all_files():
    url = f"{URL}/api/get_all_files"
    response = requests.get(url)
    result = response.json()
    return result


def dowload_file(filename_cuid):
    url = f"{URL}/api/download"
    response = requests.post(url, json=filename_cuid)
    result = response.json()
    return result


@app.route("/generate_link", methods=["GET", "POST"])
def generate_link():

    if request.method == "POST":
        if "cuid" in session:
            filename_cuid = {
                "filename": request.form['filename'],
                "cuid": session['cuid']
            }
            download_url = dowload_file(filename_cuid)
            return render_template('link.html', download_link=download_url['download_url'], filename=filename_cuid['filename'], current_type=session['type'])

        else:
            return redirect(url_for('login'))

        # return send_file(file_path, as_attachment=True)
    filename = get_all_files()
    if "type" in session:
        return render_template("downloads.html", filename=filename, current_type=session['type'])
    else:
        return redirect(url_for('login'))


def download_encrypted_link(download_token, cuid):
    url = f"{URL}{download_token}"
    data = {
        "cuid": cuid
    }
    response = requests.post(url, json=data)
    return response


@app.route("/download_file", methods=["POST"])
def download_file():
    download_token = request.form['generated_link']
    filename = request.form['filename']
    cuid = session['cuid']
    result = download_encrypted_link(download_token, cuid)
    return send_file(
        BytesIO(result.content),
        as_attachment=True,
        download_name=filename
    )


if __name__ == '__main__':
    # app.run(port=8000, debug=True)
    app.run(host='0.0.0.0', port=8000, debug=False)
