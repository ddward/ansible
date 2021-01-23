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

def insert(table,columnTuple,valueTuple):
    try:
        dbConnection = sqlite3.connect(DATABASE)
        columnTupleString = ', '.join(columnTuple)
        dbConnection.execute(
            'INSERT INTO ' + table + ' (' + columnTupleString + ') VALUES (?, ?)',
            (valueTuple)
        )
        dbConnection.commit()
    except Exception as e:
        logging.error(traceback.format_exc())

def select_one(table, return_columns, query_column, value):
    try:
        dbConnection = sqlite3.connect(DATABASE)
        result = (dbConnection.execute(
        'SELECT ' + ', '.join(return_columns) + ' FROM ' + table + ' WHERE ' + query_column + '= (?) Limit 1', 
        (value,)
        ).fetchone())
        return result
    except Exception as e:
        logging.error(traceback.format_exc())
        print("User existence check failed")

def exists(table,column,value):
    try:
        dbConnection = sqlite3.connect(DATABASE)
        result = dbConnection.execute(
        'SELECT CASE WHEN EXISTS( SELECT 1 FROM ' + table + ' WHERE ' + column + '= (?)) THEN 1 ELSE 0 END', 
        (value,)
        ).fetchone()
        if result[0] == 1:
            return True
        else:
            return False
    except Exception as e:
        logging.error(traceback.format_exc())


def update(table, update_dict, query_column, query_value):
    try:
        dbConnection = sqlite3.connect(DATABASE)
        result = (dbConnection.execute(
        'UPDATE ' + table + ' SET ' + build_set_statement(update_dict) + ' WHERE ' + query_column + '= (?)', 
        (query_value,)
        ).fetchone())
        dbConnection.commit()
        return result
    except Exception as e:
        logging.error(traceback.format_exc())

def build_set_statement(updated_field_dict):
    setItems = []
    for field in updated_field_dict:
        setItems.append(field +  ' = \'' + updated_field_dict[field] + '\'')
    setFields =  ', '.join(setItems)
    return setFields

