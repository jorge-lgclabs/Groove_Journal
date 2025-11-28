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
    retrieve_diaries,
    delete_diary_entry,
    retrieve_user_albums_ids,
    insert_diary_entry,
    remove_album_from_collection
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
    default_album = request.args.get('album')
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
    return render_template("add_album.html")


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

    #print(f"{author_user_id}\n{album_id}\n{datetime}\n{content}")

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
