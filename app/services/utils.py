from collections import defaultdict


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
