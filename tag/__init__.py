"""Tag REST API"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

api = Api(app, version='1.0', title='Tag API', description='A graffiti sharing app')
# ns = api.namespace('tag', description='Tag operations')

from tag import models, views
