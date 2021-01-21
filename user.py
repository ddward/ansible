from db import insert, exists, select_one, update
from werkzeug.security import check_password_hash, generate_password_hash
import logging
import traceback

def create_user(username,password):
    try:
        hashedPassword = generate_password_hash(password)
        insert( 'user', ('username', 'password'), (username, hashedPassword))
    except Exception as e:
        logging.error(traceback.format_exc())

def user_exists(username):
    try:
        return exists('user','username',username)
    except Exception as e:
        logging.error(traceback.format_exc())
        print("User existence check failed")

def get_user(username):
    try:
        return select_one('user',('username','password'), 'username',username)
    except Exception as e:
        logging.error(traceback.format_exc())
        print("Failed to get user")


def update_user(username,password,new_password):
    try:
        user = get_user(username)
        user_password = user[1]
        if(user is not None):
         if(check_password_hash(user_password,password)):
             newHashedPassword = generate_password_hash(new_password)
             update('user',{'password':newHashedPassword},'username',username)
    except:
        logging.error(traceback.format_exc())


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