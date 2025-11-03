from app.services.db_connection import get_connection


def retrieve_users():
    """
    Retrieve all users from the DB
    """
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    print(result)
    cursor.close()
    conn.close()

    return result
