import os

class Config:
    SECRET_KEY = os.urandom(24)  # Clave secreta para formularios
    SQLALCHEMY_DATABASE_URI = 'sqlite:///photo_album.db'  # Base de datos SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False
