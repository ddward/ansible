from db import insert, exists, select_one, update
from werkzeug.security import check_password_hash, generate_password_hash
import logging
import traceback

def create_user(username,password):
    try:
        formattedUsername = format_username(username)
        hashedPassword = generate_password_hash(password)
        insert( 'user', ('username', 'password'), (formattedUsername, hashedPassword))
    except Exception as e:
        logging.error(traceback.format_exc())

def user_exists(username):
    try:
        formattedUsername = format_username(username)
        return exists('user','username',formattedUsername)
    except Exception as e:
        logging.error(traceback.format_exc())
        print("User existence check failed")

def get_user(username):
    try:
        formattedUsername = format_username(username)
        return select_one('user',('username','password'), 'username',formattedUsername)
    except Exception as e:
        logging.error(traceback.format_exc())
        print("Failed to get user")


def update_user(username,password,new_password):
    try:
        formattedUsername = format_username(username)
        user = get_user(formattedUsername)
        user_password = user[1]
        if(user is not None):
         if(check_password_hash(user_password,password)):
             newHashedPassword = generate_password_hash(new_password)
             update('user',{'password':newHashedPassword},'username',formattedUsername)
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

def format_username(username):
    return username.lower()