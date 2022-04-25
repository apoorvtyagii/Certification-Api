from flask import Flask
from datetime import timedelta
from mongoengine import connect

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=5)
app.config.from_object("config")

connect(db='Api', host='127.0.0.1', port=27017)

from app import views, models   