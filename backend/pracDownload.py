used_tokens = set()


def generate_secure_download_url(filename):
    # Generate a secure token for the filename
    token = s.dumps({'filename': filename})

    used_tokens.add(token)
    return f'/api/secure_download/{token}'


@app.route('/api/download/<filename>', methods=['GET'])
def generate_download_url(filename):

    download_url = generate_secure_download_url(filename)
    return jsonify({'download_url': download_url})


@app.route('/api/secure_download/<token>', methods=['GET'])
def secure_download(token):
    try:
        # Verify and load the token
        data = s.loads(token)
        filename = data['filename']
        location = f"uploads/{filename}"

        # Check if the file exists before allowing the download
        if os.path.exists(location):
            used_tokens.remove(token)
            return send_file(location, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': 'Invalid or expired token'}), 401
