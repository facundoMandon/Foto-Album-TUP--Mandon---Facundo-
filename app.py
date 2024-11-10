from flask import Flask ,render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from routes import *

app.config.from_object('config.Config')



if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crea las tablas de la base de datos
    app.run(debug=True)
