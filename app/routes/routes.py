from flask import Blueprint, jsonify, render_template

from app.models import retrieve_user_collection, retrieve_users

main_blueprint = Blueprint("main", __name__)
api_blueprint = Blueprint("user", __name__, url_prefix="/api")


# ------------------#
# Page routes
# ------------------#
@main_blueprint.route("/", methods=["GET"])
def index():
    users = retrieve_users()
    return render_template("index.html", name="Test_user", users=users)


@main_blueprint.route("/collection/<int:user_id>", methods=["GET"])
def my_collection(user_id):
    albums = retrieve_user_collection(user_id)
    return render_template("collection.html", albums=albums)


@main_blueprint.route("/diary/<int:user_id>", methods=["GET"])
def my_diary(user_id):
    return render_template("diary.html")


@main_blueprint.route("/add_diary/", methods=["GET"])
def add_diary():
    albums = retrieve_user_collection(1)
    return render_template("add_diary.html", albums=albums)

@main_blueprint.route("/edit_diary/", methods=["GET"])
def edit_diary():
    albums = retrieve_user_collection(1)
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
