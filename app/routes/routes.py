from flask import Blueprint, jsonify, render_template, request

from app.models import retrieve_users

main_blueprint = Blueprint("main", __name__)
api_blueprint = Blueprint("user", __name__, url_prefix="/api")


# ------------------#
# Page routes
# ------------------#
@main_blueprint.route("/", methods=["GET"])
def index():
    users = retrieve_users()
    return render_template("index.html", name="Test_user", users=users)


# ------------------#
# API routes
# ------------------#
@api_blueprint.route("/users", methods=["GET"])
def get_all_users():
    return jsonify(retrieve_users()), 200
