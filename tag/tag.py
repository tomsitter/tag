# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, send_from_directory
from werkzeug.utils import secure_filename
from flask_restplus import Api, Resource, fields
import base64
from .geo import geocode

app = Flask(__name__) # create the application instance
api = Api(app, version='1.0', title='TAG API', description='A graffiti sharing app')

ns = api.namespace('tag', description='TAG operations')

image = api.model('Image', {
    'title': fields.String(required=True, readOnly=True, description='Title of graffiti'),
    'text': fields.String(readOnly=True, description='Description of graffiti'),
    'image': fields.String(required=True, description='Image filename'),
})

app.config.from_object(__name__) # load config from this file , tag.py

# Load default config and override config from an environment variable
app.config.update(dict(
    UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads'),
    DATABASE=os.path.join(app.root_path, 'tag.db'),
    SECRET_KEY='development key 123',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('TAG_SETTINGS', silent=True)

# Views
@api.route('/all')
class Images(Resource):
    def get(self):
        db = get_db()
        cur = db.execute('select title, text, image, lat, lon from images order by id desc')
        images = [dict(image, file=b64encode(image['image'])) for image in cur.fetchall()]
        return images

@api.route('/add')
class AddImage(Resource):
    def post(self):
        #if not session.get('logged_in'):
        #    abort(401)
        db = get_db()
        if 'image' not in request.files:
            return {'error': 'No File'}, 400
        image = request.files['image']
        if image.filename == '':
            return {'error': 'No selected file'}, 400
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(full_filename)
            lat, lon = geocode(full_filename)
            db.execute('insert into images (title, text, image, lat, lon) values (?, ?, ?, ?, ?)',
                    [request.form['title'], request.form['text'], filename, lat, lon])
            print('saved to db')
            db.commit()
            return {'Success': 'New image was successfully posted'}
        return {'Error': 'Unknown Error'}, 500

@api.route('/uploads/<filename>')
class UploadedFile(Resource):
    def get(self, filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@api.route('/login')
class Login(Resource):
    def post(self):
        content = request.get_json()
        if content['username'] != app.config['USERNAME']:
            return {'error': 'Invalid username'}, 401
        elif content['password'] != app.config['PASSWORD']:
            return {'error': 'Invalid password'}, 401
        else:
            session['logged_in'] = True
            return {'success': 'You were logged in'}

@api.route('/logout')
class Logout(Resource):
    def get(self):
        session.pop('logged_in', None)
        return {'success': 'You are now logged out'}

# Database

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    """Initialize database using schema.sql file"""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# Util

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def b64encode(filename):
    file = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb').read()
    return base64.b64encode(file).decode('utf-8')