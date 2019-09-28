import RequestParser
from db_connect import db, cursor
from flask import send_file


def get(img_name):
    return send_file(f'Data/Profile/{img_name}')