import os
from tag import app

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'tag.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(app.root_path, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
DATABASE=os.path.join(app.root_path, 'tag.db')
SECRET_KEY='development key 123'
USERNAME='admin'
PASSWORD='default'