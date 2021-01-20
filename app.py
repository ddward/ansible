import datetime
from flask import (flash, Flask, g, Markup, redirect, render_template, request,
    send_from_directory, session, url_for)
import functools
import os
import re
from secrets import token_urlsafe
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(256)

path = os.getcwd()
database = os.path.join(path, 'ansible.db')

userState = {}

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'authenticated' not in session:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

@app.route("/", methods=('GET', 'POST'))
@login_required
def index():

    currentDir = 'cloud-drive'
    uid = None

    with app.app_context():
        uid = session['user_id']
        if request.method == 'POST':
            selection = request.form['selection']
            if selection == 'home':
                pass
            elif selection == 'back':
                currentDir = userState[uid]['currentDir'].rsplit('/', 1)[0]
            else:
                if selection in userState[uid]['directoryDict']:
                    isDir = request.form['isDirectory']
                    if isDir == 'True':
                        currentDir = (userState[uid]['currentDir'] +
                        '/' + selection)
                    else:
                        return send_from_directory(
                        directory=userState[uid]['currentDir'],
                        filename=selection)
        else:
            if uid in userState:
                currentDir = userState[uid]['currentDir']
            else:
                currentDir = 'cloud-drive'

    currentPath = os.path.join(path, currentDir)

    directoryDict = {}

    with os.scandir(currentPath) as directory:
        for entry in directory:
            if not entry.name.startswith('.'):
                #stat dict reference:
                #https://docs.python.org/2/library/stat.html
                fileStats = entry.stat()
                directoryDict[entry.name] = {"is_dir" : entry.is_dir(),
                                            "size" : fileStats.st_size}

    userState[uid] = {'currentDir' : currentDir,
    'lastSeen' : datetime.datetime.now(), 'directoryDict' : directoryDict}

    return render_template('index.html',directory=directoryDict)

@app.route("/login", methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM user WHERE username = (?)', ('default',)
        ).fetchone()

        if not check_password_hash(user['password'], password):
            error = 'Incorrect password, please try again.'

        if error is None:
            session.clear()
            session['authenticated'] = 'true'
            session['user_id'] = token_urlsafe()
            return redirect(url_for('index'))

        flash(error)

    return render_template('login.html')


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            database,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db
