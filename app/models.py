from app.services.db_connection import get_connection
from app.services.utils import group_albums_tracks_artists


def retrieve_users():
    """
    Retrieve all users from the DB
    """
    conn = get_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users")
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return result


def retrieve_user_albums(user_id):
    """
    Retrieve album collection of user_id
    """
    conn = get_connection()
    if not conn:
        return []

    sql = """
    SELECT 
        a.album_id, a.album_title,
        t.track_id, t.track_title,
        aht.track_order_num,
        ar.artist_id, ar.artist_name
            FROM Albums a
            JOIN Albums_have_Owners aho ON a.album_id = aho.album_id
            JOIN Users u ON u.user_id = aho.user_id
            JOIN Albums_have_Tracks aht ON a.album_id = aht.album_id
            JOIN Tracks t ON t.track_id = aht.track_id
            JOIN Artists_have_Tracks aht2 ON t.track_id = aht2.track_id
            JOIN Artists ar ON ar.artist_id = aht2.artist_id
            WHERE u.user_id = %s
            ORDER BY a.album_id, aht.track_order_num;
    """
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, [user_id])

    result = cursor.fetchall()
    formatted_result = group_albums_tracks_artists(result)
    cursor.close()
    conn.close()

    return formatted_result


def reset_database():
    """
    Reset the database to its initial state
    """
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        # TODO: replace "your_procedure_name" with the actual stored procedure to reset_database
        cursor.callproc("your_procedure_name")
    except Exception as e:
        raise e
    finally:
        conn.commit()
        cursor.close()
        conn.close()
