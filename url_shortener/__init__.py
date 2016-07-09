from flask import Flask
import flask_utils

app = Flask(__name__, instance_relative_config=False)
app.config.from_pyfile('config.py')

from . import views
from . import assets
