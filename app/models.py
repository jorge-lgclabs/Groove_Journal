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

    sql = 'CALL sp_GetUserAlbums(%s)'
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, [user_id])
    result = cursor.fetchall()
    formatted_result = group_albums_tracks_artists(result)
    cursor.close()
    conn.close()

    return formatted_result

def retrieve_user_albums_ids(user_id):
    """
    Retrieve album_id and album_title of user_id Albums owned
    """
    conn = get_connection()
    if not conn:
        return []

    sql = 'CALL sp_GetUserJustAlbums(%s)'
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, [user_id])
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return result

def retrieve_diaries(user_id):
    """
    Retrieve diaries of user_id

    Output: list of dictionaries
     [{ diary_entry_id, diary_entry_datetime, diary_entry, album_title}, ...]
    """
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor(dictionary=True)
    try:
        sql = "CALL sp_GetUserDiaries(%s)"
        cursor.execute(sql, [user_id])
        result = cursor.fetchall()
        return result
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def retrieve_all_tracks():
    """
    retrieve all tracks in the DB

    Output: list of dictionaries
     [{track_id, track_title}, ...]
    """
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor(dictionary=True)
    try:
        sql = "CALL sp_GetTracks"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def retrieve_all_artists():
    """
    Retrieve all artists in the DB

    Output: list of dictionaries
     [{artist_id, artist_title}, ...]
    """
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor(dictionary=True)
    try:
        sql = "CALL sp_GetArtists"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()

def insert_diary_entry(author_id, album_id, entry_date, entry_content ):
    """
    Insert new diary_entry for author_id pertaining to album_id and attendant information
    """
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor(dictionary=True)
    try:
        sql = "CALL sp_InsertDiaryEntry(%s, %s, %s, %s)"
        cursor.execute(sql, [entry_content, entry_date, author_id, album_id])
        conn.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def delete_diary_entry(diary_entry_id):
    """
    Delete diary_entry of diary_entry_id
    """
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor(dictionary=True)
    try:
        sql = "CALL sp_DeleteDiaryEntry(%s)"
        cursor.execute(sql, [diary_entry_id])
        conn.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()

def reset_database():
    """
    Reset the database to its initial state
    """
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        sql = "CALL sp_ResetInitialData"
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        raise e
    finally:
        conn.commit()
        cursor.close()
        conn.close()
