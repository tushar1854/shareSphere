from connection import connection


def fetch_particular_user_files(ouid):
    try:
        conn = connection()
        cursor = conn.cursor()

        query = '''SELECT filename FROM uploaded_files WHERE ouid=%s'''
        cursor.execute(query, (ouid,))
        rows = cursor.fetchall()

        lst = []
        for row in rows:
            result_dict = {
                "filename": row[0]
            }
            lst.append(result_dict)
        return lst
    except Exception as e:
        return f"Error: {e}"
    finally:
        conn.close()
