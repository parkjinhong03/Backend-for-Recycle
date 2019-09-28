import RequestParser
from db_connect import db, cursor
from flask_jwt_extended import get_jwt_identity
from flask import send_file
from flask_restplus import reqparse
import werkzeug
import os


def get(img_name):
    return send_file(f'Data/Profile/{img_name}')


def post():
    _user = get_jwt_identity()

    parse = reqparse.RequestParser()
    parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
    args = parse.parse_args()
    audioFile = args['file']

    file_type = audioFile.filename.split('.')[1]

    file_type_list = ['jpg', 'png']
    if file_type not in file_type_list:
        return {"message": "jpg 또는 png 확장자를 가진 파일을 보내지 않음", "code": 411}, 411

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
        sql = f'UPDATE UserImage SET url = "User/Profile/{img_number}.{file_type}"'
        cursor.execute(sql)
        db.commit()

        audioFile.save(f"Data/Profile/{img_number}.{file_type}")

    else:
        os.remove(f'Data/Profile/{str(profile_data[1]).split("/")[2]}')
        audioFile.save(f"Data/Profile/{str(profile_data[1]).split('/')[2].split('.')[0]}.{file_type}")

        sql = f'UPDATE UserImage SET URL = "User/Profile/{str(profile_data[1]).split("/")[2].split(".")[0]}.{file_type}"'
        cursor.execute(sql)
        db.commit()

    return {"message": "회원 사진 변경 완료", "code": 200}, 200