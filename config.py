"""
CS 340 - Final Project
Configuration for the Flask web application.
By Jorge Rodriguez and Antonio Olaguer II
Citation:
- Adapated from Antonio Olaguer II's personal project keyfy(https://github.com/AntonioIIOlaguer/keyfy)
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    DEBUG = os.getenv("DEBUG", True)
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "Groove_Journal")
    PORT = os.getenv("PORT", 7665)
