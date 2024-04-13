from connection import connection
import uuid

# Generate UID


def generate_uid():
    return str(uuid.uuid4())


def insert_data_into_client_info(data):
    try:
        # Connect to DB
        conn = connection()
        cursor = conn.cursor()

        query = "INSERT INTO client_user_info(cuid, firstname, lastname, email, password) VALUES (%s, %s, %s, %s, %s)"
        uid = generate_uid()
        send_data = (uid,
                     data['firstname'],
                     data['lastname'],
                     data['email'],
                     data['password']
                     )
        cursor.execute(query, send_data)
        conn.commit()
        result = {
            "uid": uid,
            "email": data['email']
        }
        return result
    except Exception as e:
        return f"Error: {e}"
    finally:
        conn.close()
