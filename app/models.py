"""
CS 340 - Final Project
Models for the Flask web application, handling database interactions.
By Jorge Rodriguez and Antonio Olaguer II
Citation: All code written by authors unless otherwise noted.
"""

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

    sql = "CALL sp_GetUserAlbums(%s)"
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

    sql = "CALL sp_GetUserJustAlbums(%s)"
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


def retrieve_all_albums():
    """
    Retrieve all albums in the DB

    Output: list of dictionaries
     [{album_id, album_title}, ...]
    """
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor(dictionary=True)
    try:
        sql = "CALL sp_GetAllAlbums"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def insert_diary_entry(author_id, album_id, entry_date, entry_content):
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


def insert_album_to_collection(album_id, user_id):
    """
    Inserts specified album to specified user's collection
    """
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor(dictionary=True)
    try:
        args = [album_id, user_id]
        res = cursor.callproc("sp_InsertAlbumsHaveOwners", args)
        if res is None:
            raise Exception("Failed to insert album to collection")
        conn.commit()
        return res

    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def insert_new_album(
    album_title,
    album_label,
    album_country,
    album_year,
):
    """
    Insert new album with attendant information into the DB
    """
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        args = [
            album_title,
            album_label,
            album_country,
            album_year,
            0,  # OUT parameter placeholder
        ]

        # Insert the new album
        res = cursor.callproc("sp_InsertAlbum", args)
        if res is None:
            raise Exception("Failed to insert new album")
        conn.commit()
        album_id = res[-1]  # Get the OUT parameter (new album_id)

        return album_id

    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def insert_new_track(track_title):
    """
    Insert new track into the DB
    """
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        args = [
            track_title,
            0,  # OUT parameter placeholder
        ]
        # Insert the new track
        res = cursor.callproc("sp_InsertTrack", args)
        if res is None:
            raise Exception("Failed to insert new track")
        track_id = res[-1]  # Get the OUT parameter (new track_id)
        conn.commit()

        return track_id
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def insert_new_artist(artist_name):
    """
    Insert new artist into the DB
    """
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        args = [
            artist_name,
            0,  # OUT parameter placeholder
        ]
        # Insert the new artist
        # print(f"args: {args}")
        res = cursor.callproc("sp_InsertArtist", args)
        # print(f"res: {res}")
        if res is None:
            raise Exception("Failed to insert new artist")
        artist_id = res[-1]  # Get the OUT parameter (new artist_id)
        conn.commit()

        return artist_id
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def add_track_to_album(track_id, album_id, order_num):
    """
    Add track to album in the DB
    """
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        args = [track_id, album_id, order_num]
        cursor.callproc("sp_InsertAlbumsHaveTracks", args)

        conn.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def add_artist_to_track(artist_id, track_id):
    """
    Add artist to track in the DB
    """
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        args = [artist_id, track_id]
        cursor.callproc("sp_InsertArtistsHaveTracks", args)

        conn.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def add_artist_to_album(artist_id, album_id):
    """
    Add artist to album in the DB
    """
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        args = [album_id, artist_id]
        cursor.callproc("sp_InsertAlbumsHaveArtists", args)

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

    cursor = conn.cursor()
    try:
        sql = "CALL sp_DeleteDiaryEntry(%s)"
        cursor.execute(sql, [diary_entry_id])
        conn.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def remove_album_from_collection(input_user_id, input_album_id):
    """
    Removes specified album from specified user's collection
    """
    conn = get_connection()
    if not conn:
        return

    cursor = conn.cursor(dictionary=True)
    try:
        sql = "CALL sp_RemoveAlbumFromCollection(%s, %s)"
        cursor.execute(sql, [input_user_id, input_album_id])
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
