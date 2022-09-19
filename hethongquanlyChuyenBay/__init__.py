from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import cloudinary

app = Flask(__name__)
app.secret_key = '@(#)!@_!_#)!lda@)!('

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost/hethong?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)
login = LoginManager(app=app)

cloudinary.config(
    cloud_name='dbevamq2u',
    api_key='724382329795156',
    api_secret='Mhx_7ca9sztbZqsO--p8tG5ofMI'
)
