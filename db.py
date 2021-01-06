from getpass import getpass
import os
import sqlite3
from werkzeug.security import generate_password_hash

path = os.getcwd()
DATABASE = os.path.join(path, 'ansible.db')

def init_db():
    with app.app_context():
        db = sqlite3.connect(DATABASE)
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

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

    db = sqlite3.connect(DATABASE)
    db.execute(
        'INSERT INTO user (username, password) VALUES (?, ?)',
        ('default', generate_password_hash(password))
    )
    db.commit()
