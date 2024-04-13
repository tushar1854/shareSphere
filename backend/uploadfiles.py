from connection import connection


def upload_filess(ouid, file, app):
    try:
        conn = connection()
        cursor = conn.cursor()
        # Check user is registered or not
        query = '''SELECT ouid, firstname FROM operation_user_info WHERE ouid = %s'''
        cursor.execute(query, (ouid,))
        row = cursor.fetchone()

        if row:
            upload_file_query = '''INSERT INTO uploaded_files(ouid, filename, location) VALUES(%s,%s,%s)'''
            data = (
                ouid,
                file.filename,
                f"{app.config['UPLOAD_FOLDER']}/{file.filename}"
            )
            cursor.execute(upload_file_query, data)
            conn.commit()
            # Save the uploaded file to the specified folder
            file.save(app.config['UPLOAD_FOLDER'] + '/' + file.filename)
            result = {
                "message": 'File uploaded successfully!'
            }
            return result

        else:
            result = {
                "message": 'Unsuccessful Upload'
            }
            return result

    except Exception as e:
        result = {
            "message": f"{e}"
        }
        return result
