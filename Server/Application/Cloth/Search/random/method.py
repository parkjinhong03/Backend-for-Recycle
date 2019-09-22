import RequestParser
from db_connect import db, cursor
from flask import send_file


def get():
    return send_file('Data/Image/T-shirt1.jpg')