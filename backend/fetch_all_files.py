from connection import connection


def fetch_all_files():
    try:
        conn = connection()
        cursor = conn.cursor()

        query = '''SELECT uf.filename, uf.location, oui.firstName, uf.count, oui.lastName FROM uploaded_files AS uf INNER JOIN operation_user_info AS oui
                ON uf.ouid = uf.ouid ORDER BY uf.createdat DESC'''
        cursor.execute(query)
        rows = cursor.fetchall()

        lst = []
        for row in rows:
            result_dict = {
                "filename": row[0],
                "location": row[1],
                "firstname": row[2],
                "count": row[3],
                "lastname": row[4]
            }
            lst.append(result_dict)
        return lst
    except Exception as e:
        return f"Error: {e}"
    # finally:
        # pass
        # return "sai"
        # conn.close()
