# all the imports
import os
import base64

from flask import request, session, send_from_directory
from werkzeug.utils import secure_filename
from flask_restplus import Resource
from .geo import geocode
from .models import Image
from tag import app, api, db


@api.route('/all')
class Images(Resource):
    def get(self):
        # TODO: Get access to database
        #images = [dict(image, file=b64encode(image['image'])) for image in cur.fetchall()]
        images = [{'test': 1}, {'test': 2}]
        return images

@api.route('/add')
class AddImage(Resource):
    def post(self):
        #if not session.get('logged_in'):
        #    abort(401)
         # TODO: Get access to database
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
            i = Image(
                title=request.form['title'],
                description=request.form['description'],
                filename=request.form['filename'],
                latitude=lat,
                longitude=lon
            )
            db.session.add(i)
            db.session.commit()            
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


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

# Util

def allowed_file(filename):
    allowed_extensions = set(['png', 'jpg', 'jpeg'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def b64encode(filename):
    file = open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb').read()
    return base64.b64encode(file).decode('utf-8')