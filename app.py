from cryptography.fernet import Fernet
import datetime
from flask import (flash, Flask, g, Markup, redirect, render_template, request,
    send_from_directory, session, url_for)
import functools
import logging
import os
from secrets import token_urlsafe
import sqlite3
import sys
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from build_dir import build_dir
import sanitize_path
from db import get_db, create_user, user_exists
import html


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(256) # TODO: change to environemnt variable
app.config["CRYPTO_KEY"] = Fernet.generate_key() # TODO put this somewhere where it wont update often possibly environmnet analize impact of changing.

path = os.getcwd()
database = os.path.join(path, 'ansible.db')

db = get_db(app)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'authenticated' not in session:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

@app.route('/', defaults={'loc': ""}, methods=('GET',))
@app.route('/<path:loc>', methods=('GET',))
@login_required
def ansible(loc):
    logging.debug('made it here')
    sanitize_path.sanitize(loc)

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
        username = request.form['username']
        password = request.form['password']
        db = get_db(app)
        error = None

        user = db.execute(
            'SELECT * FROM user WHERE username = (?)', (username,)
        ).fetchone()
        if user is not None:
            if not check_password_hash(user['password'], password):
                error = 'Incorrect password, please try again.'
        else:
            error = 'User not found'

        if error is None:
            session.clear()
            session['authenticated'] = 'true'
            session['user_id'] = token_urlsafe()
            return redirect(url_for('ansible'))

        flash(error)

    return render_template('login.html')

@app.route("/signup", methods=('GET','POST'))
def signup():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        error = None

        if not user_exists(username):
            create_user(username,password)
        else:
            error = 'Username already exists.'

        if  error is None:
            return redirect(url_for('login'))

        flash(error)


    return render_template('signup.html')

@app.route("/logout", methods=('GET',))
def logout():
    del session['authenticated']
    return redirect(url_for('login'))



