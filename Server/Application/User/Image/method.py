import RequestParser
from db_connect import db, cursor
from flask_jwt_extended import get_jwt_identity
from flask import send_file
from flask_restplus import reqparse
import werkzeug
import os
import base64


def get(img_name):
    return send_file(f'Data/Profile/{img_name}')


def post():
    _user = get_jwt_identity()

    img_data = str(RequestParser.parser('binary')[0])

    path_dir = f'Data/Profile'
    file_list = os.listdir(path_dir)
    file_list.sort()

    img_number = 0
    for i in file_list:
        try:
            int(i.split('.')[0])
        except:
            continue

        img_number = int(i.split('.')[0]) + 1

    sql = f'SELECT * FROM UserImage WHERE name="{_user}"'
    cursor.execute(sql)

    profile_data = cursor.fetchone()

    if str(profile_data[1]).split('/')[2] == 'default.jpg':
        sql = f'UPDATE UserImage SET url = "User/Profile/{img_number}.png WHERE name = "{_user}"'
        cursor.execute(sql)
        db.commit()

        with open(f'Data/Profile/{img_number}.png', 'wb') as f:
            f.write(base64.b64decode(img_data))

    else:
        os.remove(f'Data/Profile/{str(profile_data[1]).split("/")[2]}')

        with open(f"Data/Profile/{str(profile_data[1]).split('/')[2].split('.')[0]}.png", 'wb') as f:
            f.write(base64.b64decode(img_data))

    return {"message": "회원 사진 변경 완료", "code": 200}, 200