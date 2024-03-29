import RequestParser
from db_connect import connect
from flask import request
from werkzeug import security
from flask_jwt_extended import get_jwt_identity
from flask_restplus import reqparse
import werkzeug
import os
import datetime
import base64


def delete(cloth_type):
    '''
    :param cloth_type:
    :return: status code
    200 - 제품 등록 취소 성공.
    410 - {type} path에 Shirts, Shoes, Pants, Accessory 이외의 값을 줌
    411 - swagger docs에 나와있는 대로 params을 전달해 주세요.
    412 - 해당 url에 대해 제품이 존재하지 않거나 요청한 유저의 제품이 아님
    '''

    db, cursor = connect()
    type_list = ['Shirts', 'Shoes', 'Pants', 'Accessory']
    if cloth_type not in type_list:
        return {"message": "{type} path에 Shirts, Shoes, Pants, Accessory 이외의 값을 줌", "code": 410}, 410

    ImageUrl = str(RequestParser.parser('url')[0])

    user_name = get_jwt_identity()

    sql = f'SELECT * FROM {cloth_type}List WHERE User = "{user_name}" AND Url = "{ImageUrl}"'
    cursor.execute(sql)
    select_data = cursor.fetchone()
    print(select_data)

    if select_data is None:
        return {"message": "해당 url에 대해 제품이 존재하지 않거나 요청한 유저의 제품이 아님", "code": 412}, 412

    if int(select_data[7]) == 1:
        return {"message": "해당 url에 대한 제품은 이미 판매된 제품임", "code": 413}, 413

    sql = f'DELETE FROM {cloth_type}List WHERE User = "{user_name}" AND Url = "{ImageUrl}"'
    cursor.execute(sql)
    db.commit()

    path = f'Data/Image/{cloth_type}/{ImageUrl.split("/")[3]}'
    os.remove(path)

    sql = f'SELECT * FROM ReservationData WHERE url = "{ImageUrl}"'
    cursor.execute(sql)
    cancle_data = list(cursor.fetchall())

    for i in cancle_data:
        sql = f'INSERT INTO ReservationCancelData (name, url, register_name, register_title) VALUES("{i[0]}", "{i[1]}", "{i[2]}", "{i[3]}")'
        cursor.execute(sql)
        db.commit()

    sql = f'DELETE FROM ReservationData WHERE url = "{ImageUrl}"'
    cursor.execute(sql)
    db.commit()

    return {"message": "제품 등록 취소 완료", "code": 200}, 200


def post(cloth_type):
    '''
    옷을 등록하주는 POST Method
    :return: status code
    410 - {type} path에 Shirts, Shoes, Pants, Accessory 이외의 값을 줌
    411 - 전달한 파일의 확장자가 jpg, png 외의 파일임
    412 - price 값에 문자열이 포함되어있음
    413 - size 값으로 올바른 데이터을 넣지 않았음
    414 - 매개변수로 주지 않은 값이 있음
    200 - 제품 등록에 완료함
    '''

    db, cursor = connect()
    type_list = ['Shirts', 'Shoes', 'Pants', 'Accessory']
    if cloth_type not in type_list:
        db.close()
        return {"message": "{type} path에 Shirts, Shoes, Pants, Accessory 이외의 값을 줌", "code": 410}, 410

    user_name = get_jwt_identity()

    cloth_title, cloth_description, cloth_price, cloth_size, first_date, status, binary = RequestParser.parser('title', 'description', 'price', 'size', 'first_date', 'status', 'binary')
    print(user_name, cloth_title, cloth_description, cloth_price, cloth_size, first_date)

    if None in [cloth_title, cloth_description, cloth_price, cloth_size, first_date, status]:
        db.close()
        return {"message": "docs 문서에서 나온 parmas 들을 모두 주세용", "code": 414}, 414

    try:
        int(cloth_price)
    except ValueError:
        db.close()
        return {"message": "price 값에 문자열이 포함되어있음.", "code": 412}, 412

    path_dir = f'Data/Image/{cloth_type}'
    file_list = os.listdir(path_dir)
    file_list.sort()
    print(file_list)

    img_number = 0
    for i in file_list:
        img_number = int(i.split('.')[0]) + 1

    url = f'Cloth/Image/{cloth_type}/{img_number}.png'

    for i in type_list:
        sql = f'CREATE TABLE {i}List (' \
               'User TEXT NOT NULL,'\
               'Url TEXT NOT NULL,' \
               'Title TEXT NOT NULL,' \
               'Description TEXT NOT NULL,' \
               'Price INT(11) NOT NULL,' \
               'Size TEXT NOT NULL,' \
               'FirstDate INT(11) NOT NULL,' \
               'SellStatus BOOL DEFAULT 0 NOT NULL,' \
               'ImageNumber INT(11) NOT NULL,' \
               'CreateData TEXT NOT NULL,' \
               'Status varchar(100) NOT NULL' \
               ')'
        try:
            cursor.execute(sql)
        except:
            pass

    now = datetime.datetime.now()
    sql = f'INSERT INTO {cloth_type}List ' \
        '(User, Url, Title, Description, Price, Size, FirstDate, ImageNumber, CreateData, Status)' \
        f'VALUES("{user_name}", "{url}", "{cloth_title}", "{cloth_description}", "{cloth_price}", "{cloth_size}", "{first_date}", "{img_number}", {now.strftime("%Y%m%d%H%M%S")}, "{status}")'
    cursor.execute(sql)
    db.commit()

    with open(f'Data/Image/{cloth_type}/{img_number}.png', 'wb') as f:
        f.write(base64.b64decode(binary))

    db.close()
    return {"message": "제품 등록에 성공하였습니다", "code": 200}, 200