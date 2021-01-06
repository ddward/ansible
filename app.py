from cryptography.fernet import Fernet
import datetime
from flask import (flash, Flask, g, Markup, redirect, render_template, request,
    send_from_directory, session, url_for)
import functools
import logging
import os
import re
from secrets import token_urlsafe
import sqlite3
import sys
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(256) # TODO: change to environemnt variable
app.config["CRYPTO_KEY"] = Fernet.generate_key() # TODO put this somewhere where it wont update often possibly environmnet analize impact of changing.

path = os.getcwd()
database = os.path.join(path, 'ansible.db')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'authenticated' not in session:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

@app.route('/', defaults={'loc': ""}, methods=('GET',))
@app.route('/<path:loc>', methods=('GET',))
#@login_required
def ansible(loc):
    logging.debug('made it here')
    # escape nasty double-dots
    loc = re.sub(r'\.\.', '', loc)
    # then remove any duplicate slashes
    loc = re.sub(r'(/)\1+', r'\1', loc)
    # then remove any leading slashes and dots
    while(loc and (loc[0] == '/' or loc[0] == '.')):
        loc = loc[1:]

    # TODO: if loc is empty return the home directory for the node
    # possible security concern - could ask for a higher level node
    # TODO: for future addition of link sending - store encrypted version
    # of top level directory in session can possibly use a werkzeug module
    # TODO: check if input is an encrypted link (use a /share/ or something to indicate)
    # TODO: process encrypted link
    # TODO: process a normal link
    # TODO: get the the home directory

    # TODO: authenticate the requested directory

    logging.debug(loc)

    currentDir = os.path.join('cloud-drive', loc) #update to be maliable for sharing

    currentPath = os.path.join(path, currentDir)

    logging.debug(os.path.splitext(currentPath)[1])
    logging.debug(currentDir)
    logging.debug(path)
    logging.debug(currentPath)
    logging.debug(loc)

    fileExtension = os.path.splitext(currentPath)[1]
    if fileExtension:
        splitUrl = currentPath.rsplit('/', 1)
        localDir = splitUrl[0]
        filename = splitUrl[1]
        absPath = os.path.join(path, 'cloud-drive', localDir)
        return send_from_directory(directory=absPath, filename=filename)

    directoryDict = build_dir(currentPath)

    return render_template('index-alt.html', directory=directoryDict, curDir=loc)

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
            return redirect(url_for('ansible'))

        flash(error)

    return render_template('login.html')

@app.route("/logout", methods=('GET',))
def logout():
    del session['authenticated']
    return redirect(url_for('login'))

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            database,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def build_dir(curPath):
    directoryDict = {}
    with os.scandir(curPath) as directory:
        for entry in directory:
            #dont include shortcuts and hidden files
            if not entry.name.startswith('.'):
                #stat dict reference:
                #https://docs.python.org/2/library/stat.html
                fileStats = entry.stat()
                directoryDict[entry.name] = {"is_dir" : entry.is_dir(),
                                            "size" : fileStats.st_size}
    return directoryDict
