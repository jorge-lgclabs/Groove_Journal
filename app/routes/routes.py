from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.models import (
    reset_database,
    retrieve_all_artists,
    retrieve_all_tracks,
    retrieve_user_albums,
    retrieve_users,
)

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

    # TODO: Unccomment the line below to retrieve actual diary entries from the database.
    # diaries = retrieve_user_albums(user_id)

    # For demo purposes, using hardcoded diary entries remove once DB retrieval is implemented.
    diaries = [
        {
            "diary_entry_id": 1,
            "diary_entry_date_time": "2024-01-01 10:00:00",
            "diary_entry": "This is a sample diary entry.",
            "album_title": "Sample Album",
        },
        {
            "diary_entry_id": 2,
            "diary_entry_date_time": "2024-01-02 11:00:00",
            "diary_entry": "Another diary entry example.",
            "album_title": "Another Album",
        },
    ]

    return render_template("diary.html", diaries=diaries)


@main_blueprint.route("/all_artists", methods=["GET"])
def all_artists():
    """
    Retrieve all artists from the database and render them on the artists page.
    """

    # TODO: Unccomment the line below to retrieve actual artists from the database.
    # artists = retrieve_all_artists()

    # For demo purposes, using hardcoded artists entries remove once DB retrieval is implemented.
    artists = [
        {"artist_id": 1, "artist_name": "Taylor Swift"},
        {"artist_id": 2, "artist_name": "Ed Sheeran"},
        {"artist_id": 3, "artist_name": "Adele"},
    ]

    return render_template("artists.html", artists=artists)


@main_blueprint.route("/all_tracks", methods=["GET"])
def all_tracks():
    """
    Retrieve all artists from the database and render them on the artists page.
    """

    # TODO: Unccomment the line below to retrieve actual tracks from the database.
    # tracks = retrieve_all_tracks()

    # For demo purposes, using hardcoded tracks entries remove once DB retrieval is implemented.
    tracks = [
        {"track_id": 1, "track_title": "Track One"},
        {"track_id": 2, "track_title": "Track Two"},
        {"track_id": 3, "track_title": "Track Three"},
    ]

    return render_template("tracks.html", tracks=tracks)


@main_blueprint.route("/add_diary/", methods=["GET"])
def add_diary():
    albums = retrieve_user_albums(1)
    return render_template("add_diary.html", albums=albums)


@main_blueprint.route("/edit_diary/", methods=["GET"])
def edit_diary():
    albums = retrieve_user_albums(1)
    return render_template("edit_diary.html", albums=albums)


@main_blueprint.route("/add_album/", methods=["GET"])
def add_album():
    return render_template("add_album.html")


# ------------------#
# API routes
# ------------------#
@api_blueprint.route("/users", methods=["GET"])
def get_all_users():
    return jsonify(retrieve_users()), 200


@api_blueprint.route("/resetDB", methods=["GET"])
def reset_db():
    # TODO: uncomment the line below to enable DB reset.
    # reset_database()
    print("Database has been reset.")
    return redirect(url_for("main.index"))


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
