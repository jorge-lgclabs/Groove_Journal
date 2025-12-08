"""
CS 340 - Final Project
Database connection service for the Flask web application.
By Jorge Rodriguez and Antonio Olaguer II
Citation: All code written by authors unless otherwise noted.
"""

import mysql.connector
from flask import current_app
from mysql.connector import Error


# Function to get a new connection
def get_connection():
    try:
        connection = mysql.connector.connect(
            host=current_app.config["DB_HOST"],
            user=current_app.config["DB_USER"],
            password=current_app.config["DB_PASSWORD"],
            database=current_app.config["DB_NAME"],
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
