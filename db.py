from getpass import getpass
import os
import sqlite3
from werkzeug.security import generate_password_hash
from flask import g
import traceback
import logging

path = os.getcwd()
DATABASE = os.path.join(path, 'ansible.db')

def init_db():
    with app.app_context():
        db = sqlite3.connect(DATABASE)
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db(app):
    with app.app_context():
        if 'db' not in g:
            g.db = sqlite3.connect(
                DATABASE,
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row

        return g.db


def gen_default_user():

    while(True):
        password = getpass(prompt='Create a password, at least 8 characters: ')
        password2 = getpass(prompt='Confirm password: ')
        if password == password2:
            if len(password) < 8:
                print('Password must be at least 8 characters.')
            else:
                break
        else:
            print('Passwords do not match')
    try:
        create_user('default',password)
    except:
        logging.error(traceback.format_exc())

def create_user(username,password):
    try:
        db = sqlite3.connect(DATABASE)
        db.execute(
            'INSERT INTO user (username, password) VALUES (?, ?)',
            (username, generate_password_hash(password))
        )
        db.commit()
    except Exception as e:
        logging.error(traceback.format_exc())

def user_exists(username):
    try:
        db = sqlite3.connect(DATABASE)
        result = (db.execute(
        'SELECT CASE WHEN EXISTS( SELECT 1 FROM user WHERE username = (?)) THEN 1 ELSE 0 END', 
        (username,)
        ).fetchone())
        if result[0] == 1:
            return True
        else:
            return False
    except Exception as e:
        logging.error(traceback.format_exc())
        print("User existence check failed")

def get_user(username):
    try:
        db = sqlite3.connect(DATABASE)
        result = (db.execute(
        'SELECT 1 FROM user WHERE username = (?)', 
        (username,)
        ).fetchone())
        print(result)
        return result
    except Exception as e:
        logging.error(traceback.format_exc())
        print("User existence check failed")

