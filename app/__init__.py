"""
CS340 - Final Project
Initialization of the Flask application.
By Jorge Rodriguez and Antonio Olaguer II
Citation: All code written by authors unless otherwise noted.
"""

from flask import Flask

from config import Config

from .routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_routes(app)

    return app
