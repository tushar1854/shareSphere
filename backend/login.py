from connection import connection


def send_data_for_login(data):
    conn = connection()
    cursor = conn.cursor()
    # Check for operation user
    operation_query = '''SELECT ouid, email FROM operation_user_info WHERE email=%s and password=%s'''
    info = (
        data['email'],
        data['password']
    )
    cursor.execute(operation_query, info)
    row = cursor.fetchone()

    if row:
        # Insert into login
        login_insert_query = '''INSERT INTO login_info(uid, email, type) VALUES(%s,%s,%s)'''
        operation_login_data = (
            row[0],
            data['email'],
            "operation"
        )
        cursor.execute(login_insert_query, operation_login_data)
        conn.commit()
        result = {
            "message": "data inserted successfully",
            "uid": row[0],
            "type": "operation",
            "success": 1
        }
        return result
    else:
        # Check for client user
        operation_query = '''SELECT cuid, email FROM client_user_info WHERE email=%s and password=%s'''
        info = (
            data['email'],
            data['password']
        )
        cursor.execute(operation_query, info)
        row = cursor.fetchone()
        if row:
            # Insert into login
            login_insert_query = '''INSERT INTO login_info(uid, email, type) VALUES(%s,%s,%s)'''
            client_login_data = (
                row[0],
                data['email'],
                "client"
            )
            cursor.execute(login_insert_query, client_login_data)
            conn.commit()
            result = {
                "message": "data inserted successfully",
                "uid": row[0],
                "type": "client",
                "success": 1
            }
            return result

    result = {
        "message": "incorrect credentials",
        "success": 0
    }
    return result
