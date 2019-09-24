import RequestParser
from db_connect import db, cursor
from flask import send_file


def get(type, img_name):
    type_list = ['Shirts', 'Pants', 'Accessory', 'Shoes']
    if type not in type_list:
        return {'Message': 'type 경로를 Shirts, Pants, Accessory, Shoes, Else 중 하나로 해주세요'}
    return send_file(f'Data/Image/{type}/{img_name}')