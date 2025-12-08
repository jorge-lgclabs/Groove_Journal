"""
CS 340 - Final Project
Entry point for running the Flask web application.
By Jorge Rodriguez and Antonio Olaguer II
Citation: All code written by authors unless otherwise noted.
"""

from flask import current_app

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=15506)
