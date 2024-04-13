from connection import connection


def download_count_increase(location):
    conn = connection()
    cursor = conn.cursor()
    # Check for operation user
    operation_query = '''UPDATE uploaded_files SET count = count + 1 WHERE location = %s'''
    info = (
        location,
    )
    cursor.execute(operation_query, info)
    conn.commit()
