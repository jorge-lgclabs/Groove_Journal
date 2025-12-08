"""
CS340 - Final Project
Utility functions for the Flask web application.
By Jorge Rodriguez and Antonio Olaguer II
Citation: All code written by authors unless otherwise noted.
"""

from collections import defaultdict

from flask import flash


def group_albums_tracks_artists(rows):
    """
    A helper function for parsing through the SQL response of retrieve_user_collection().
    This groups multiple entries of albums into one and groups the tracks per album and lists it's artist.
    [
        {
            'album_title': 'Album A',
            'tracks': [
                {'track_title': 'Track 1', 'artists': ['Artist 1', 'Artist 2']},
                {'track_title': 'Track 2', 'artists': ['Artist 3']}
            ]
        },
        {
            'album_title': 'Album B',
            'tracks': [
                {'track_title': 'Track 1', 'artists': ['Artist 4']}
            ]
        }
    ]
    """

    # Prevent missing keys by utilizing defaultdict
    albums = defaultdict(lambda: {"tracks": defaultdict(lambda: {"artists": []})})

    for row in rows:
        album_id = row["album_id"]
        track_id = row["track_id"]

        # Album info

        albums[album_id].update({"album_title": row["album_title"]})

        # Track info
        albums[album_id]["tracks"][track_id].update(
            {
                "track_title": row["track_title"],
                "track_order_num": row["track_order_num"],
            }
        )

        # Artists
        albums[album_id]["tracks"][track_id]["artists"].append(row["artist_name"])

    # Convert to list and sort tracks by track_order_num
    album_list = []
    for key, album in albums.items():
        track_list = list(album["tracks"].values())
        track_list.sort(key=lambda x: x["track_order_num"])  # sort by track order
        album["tracks"] = track_list
        album["album_id"] = key
        album_list.append(album)

    return album_list


def handle_errors(e):
    """
    A generic error handler that can be expanded for different error types.
    """
    if "Duplicate entry" in str(e):
        flash("Duplicate entry error: The record already exists.", "warning")
    else:
        flash(f"An unexpected error occurred: {str(e)}", "error")


def extract_tracks(form_data):
    """
    Extracts track information from the form data.
    Args: form_data (ImmutableMultiDict): The form data from the request.
    Returns: list: A list of dictionaries representing tracks and their associated artists.
    """
    tracks = {}

    for key, value in form_data.items():
        if key.startswith("tracks"):
            # Parse the key to extract the index and field name
            parts = key.split("[")
            index = int(parts[1][:-1])  # Extract the index (e.g., 0, 1)
            field = (
                parts[2][:-1] if len(parts) > 2 else None
            )  # Extract the field name (e.g., track_name, existing_artists)

            # Initialize the track dictionary if it doesn't exist
            if index not in tracks:
                tracks[index] = {}

            # Handle multiple values for existing_artists[]
            if field == "existing_artists":
                tracks[index].setdefault(field, []).append(value)
            if field == "track_name":
                tracks[index][field] = value
            else:
                new_artist_list = [artist.strip() for artist in value.split(",")]
                if new_artist_list == [""]:
                    continue
                tracks[index][field] = new_artist_list

    # Convert the tracks dictionary to a list
    tracks_list = [tracks[i] for i in tracks]
    return tracks_list
