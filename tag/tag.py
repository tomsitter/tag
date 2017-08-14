# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__) # create the application instance
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
@app.route('/')
def show_images():
    db = get_db()
    cur = db.execute('select title, text, image from images order by id desc')
    images = cur.fetchall()
    return render_template('show_images.html', images=images)

@app.route('/add', methods=['POST'])
def add_image():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    if 'image' not in request.files:
        flash('No Image!')
        return redirect(url_for('show_images'))
    image = request.files['image']
    if image.filename == '':
        flash('No selected file')
        return redirect(url_for('show_images'))
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        db.execute('insert into images (title, text, image) values (?, ?, ?)',
                    [request.form['title'], request.form['text'], filename])
        db.commit()
        flash('New image was successfully posted')
    return redirect(url_for('show_images'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_images'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_images'))

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