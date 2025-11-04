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
    print(albums)
    return render_template("collection.html", albums=albums)


# ------------------#
# API routes
# ------------------#
@api_blueprint.route("/users", methods=["GET"])
def get_all_users():
    return jsonify(retrieve_users()), 200
