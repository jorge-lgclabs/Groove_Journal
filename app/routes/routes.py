from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.models import (
    add_artist_to_album,
    add_artist_to_track,
    add_track_to_album,
    delete_diary_entry,
    insert_album_to_collection,
    insert_diary_entry,
    insert_new_album,
    insert_new_artist,
    insert_new_track,
    remove_album_from_collection,
    reset_database,
    retrieve_all_albums,
    retrieve_all_artists,
    retrieve_all_tracks,
    retrieve_diaries,
    retrieve_user_albums,
    retrieve_user_albums_ids,
    retrieve_users,
)
from app.services.utils import extract_tracks, handle_errors

main_blueprint = Blueprint("main", __name__)
api_blueprint = Blueprint("user", __name__, url_prefix="/api")


# ------------------#
# Page routes
# ------------------#
@main_blueprint.route("/", methods=["GET"])
def index():
    """
    Render the home page with user information and list of users.
    """

    # Demo purposes: set default user in session
    user_id = session.get("user_id", 1)
    user_fname = session.get("user_fname", "jorge")
    user_lname = session.get("user_lname", "Rodriguez")
    users = retrieve_users()
    return render_template(
        "index.html",
        user_id=user_id,
        user_fname=user_fname,
        user_lname=user_lname,
        users=users,
    )


@main_blueprint.route("/albums", methods=["GET"])
def my_albums():
    """
    Retrieve albums for the logged-in user and render them on the albums page.
    """
    user_id = session.get("user_id", 1)
    albums = retrieve_user_albums(user_id)

    return render_template("albums.html", albums=albums)


@main_blueprint.route("/diary", methods=["GET"])
def my_diary():
    """
    Retrieve diary entries for the logged-in user and render them on the diary page.
    """
    # Demo purposes: set default user in session
    user_id = session.get("user_id", 1)
    diaries = retrieve_diaries(user_id)

    return render_template("diary.html", diaries=diaries)


@main_blueprint.route("/all_artists", methods=["GET"])
def all_artists():
    """
    Retrieve all artists from the database and render them on the artists page.
    """
    artists = retrieve_all_artists()

    return render_template("artists.html", artists=artists)


@main_blueprint.route("/all_tracks", methods=["GET"])
def all_tracks():
    """
    Retrieve all artists from the database and render them on the artists page.
    """
    tracks = retrieve_all_tracks()

    return render_template("tracks.html", tracks=tracks)


@main_blueprint.route("/add_diary/", methods=["GET"])
def add_diary():
    default_album = request.args.get("album")
    if not default_album:
        default_album = 0
    user_id = session.get("user_id", 1)
    albums = retrieve_user_albums_ids(user_id)
    return render_template("add_diary.html", default_album=default_album, albums=albums)


@main_blueprint.route("/edit_diary/", methods=["GET"])
def edit_diary():
    albums = retrieve_user_albums(1)
    return render_template("edit_diary.html", albums=albums)


@main_blueprint.route("/add_album/", methods=["GET"])
def add_album():
    albums = retrieve_all_albums()
    artists = retrieve_all_artists()
    tracks = retrieve_all_tracks()
    return render_template(
        "add_album.html", albums=albums, artists=artists, tracks=tracks
    )


# ------------------#
# API routes
# ------------------#
@api_blueprint.route("/users", methods=["GET"])
def get_all_users():
    return jsonify(retrieve_users()), 200


@api_blueprint.route("/resetDB", methods=["GET"])
def reset_db():
    reset_database()
    return redirect(url_for("main.index"))


@api_blueprint.route("/add_diary_entry", methods=["POST"])
def api_add_diary_entry():
    author_user_id = session.get("user_id", 1)
    album_id = request.form.get("album_id")
    datetime = request.form.get("entry_datetime")
    content = request.form.get("entry_content")

    datetime = datetime.replace("T", " ")

    # print(f"{author_user_id}\n{album_id}\n{datetime}\n{content}")

    insert_diary_entry(author_user_id, album_id, datetime, content)

    return redirect(url_for("main.my_diary"))


@api_blueprint.route("/delete_diary", methods=["POST"])
def api_delete_diary_entry():
    diary_entry_id = request.form.get("diary_entry_id")
    delete_diary_entry(diary_entry_id)
    return redirect(url_for("main.my_diary"))


@api_blueprint.route("/remove_album", methods=["POST"])
def api_remove_album_from_collection():
    user_id = session.get("user_id", 1)
    album_id = request.form.get("album_id")
    remove_album_from_collection(user_id, album_id)
    return redirect(url_for("main.my_albums"))


@api_blueprint.route("/select_user", methods=["POST"])
def select_user():
    user_id = request.form.get("user_id")
    user_fname = request.form.get("user_fname")
    user_lname = request.form.get("user_lname")

    if user_id:
        session["user_id"] = user_id
        session["user_fname"] = user_fname
        session["user_lname"] = user_lname

    return redirect(url_for("main.index"))


@api_blueprint.route("/add_existing_album", methods=["POST"])
def api_add_existing_album():
    user_id = session.get("user_id", 1)
    existing_album_id = request.form.get("existing_album")
    try:
        insert_album_to_collection(existing_album_id, user_id)
    except Exception as e:
        handle_errors(e)
        return redirect(url_for("main.my_albums"))

    return redirect(url_for("main.my_albums"))


@api_blueprint.route("/add_new_album", methods=["POST"])
def api_add_new_album():
    user_id = session.get("user_id", 1)
    album_title = request.form.get("album_title")
    album_label = request.form.get("album_label")
    album_country = request.form.get("album_country")
    album_year = request.form.get("album_year")
    tracks = extract_tracks(request.form)  # Utility function to parse track data
    running_new_artists = {}  # A running dict of new {artist:artist_id} inserted for this album
    running_artist_album = []  # A running list of which artists have been correlated to this album

    # print(f"Tracks: {tracks}")

    try:
        # Insert new album
        new_album_id = insert_new_album(
            album_title,
            album_label,
            album_country,
            album_year,
        )
        # Add album to user's collection
        insert_album_to_collection(new_album_id, user_id)

        # Insert tracks and link artists
        for index, track in enumerate(tracks):
            track_name = track.get("track_name")
            existing_artists = track.get("existing_artists", [])
            new_artists = track.get("new_artists", [])

            if not track_name:
                continue

            # Insert new track
            track_id = insert_new_track(track_name)
            add_track_to_album(track_id, new_album_id, index + 1)

            if existing_artists:
                # Link existing artists to track and album
                for artist_id in existing_artists:
                    add_artist_to_track(artist_id, track_id)
                    # Check if this artist has already been correlated with this album
                    if artist_id not in running_artist_album:
                        add_artist_to_album(artist_id, new_album_id)
                        running_artist_album.append(artist_id)

            if new_artists:
                # Create new artists and link to track
                for artist_name in new_artists:
                    # Check for already inserted artist from this album
                    if artist_name in running_new_artists:
                        artist_id = running_new_artists[artist_name]
                    else:
                        artist_id = insert_new_artist(artist_name)  # If artist doesn't exist, insert it
                        running_new_artists[artist_name] = artist_id
                    # Check if this artist has already been correlated with this album
                    if artist_id not in running_artist_album:
                        add_artist_to_album(artist_id, new_album_id)  # Add this artist to this album only once
                        running_artist_album.append(artist_id)
                    # Finally, correlate this artist with this track
                    add_artist_to_track(artist_id, track_id)


    except Exception as e:
        handle_errors(e)
        return redirect(url_for("main.my_albums"))

    return redirect(url_for("main.my_albums"))
