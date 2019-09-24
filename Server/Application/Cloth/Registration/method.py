import RequestParser
from db_connect import db, cursor
from flask import request
from werkzeug import security
from flask_jwt_extended import get_jwt_identity
from flask_restplus import reqparse
import werkzeug
import os


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

    type_list = ['Shirts', 'Shoes', 'Pants', 'Accessory']
    if cloth_type not in type_list:
        return {"message": "{type} path에 Shirts, Shoes, Pants, Accessory 이외의 값을 줌", "code": 410}, 410

    user_name = get_jwt_identity()

    cloth_title, cloth_description, cloth_price, cloth_size, first_date = RequestParser.parser('title', 'description', 'price', 'size', 'first_date')
    print(user_name, cloth_title, cloth_description, cloth_price, cloth_size, first_date)

    if None in [cloth_title, cloth_description, cloth_price, cloth_size, first_date]:
        return {"message": "docs 문서에서 나온 parmas 들을 모두 주세용", "code": 414}, 414

    parse = reqparse.RequestParser()
    parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
    args = parse.parse_args()
    audioFile = args['file']

    file_type = audioFile.filename.split('.')[1]

    file_type_list = ['jpg', 'png']
    if file_type not in file_type_list:
        return {"message": "jpg 또는 png 확장자를 가진 파일을 보내지 않음", "code": 411}, 411

    try:
        int(cloth_price)
    except ValueError:
        return {"message": "price 값에 문자열이 포함되어있음.", "code": 412}, 412

    path_dir = f'Data/Image/{cloth_type}'
    file_list = os.listdir(path_dir)
    file_list.sort()
    print(file_list)

    img_number = 0
    for i in file_list:
        img_number = int(i.split('.')[0]) + 1

    url = f'Cloth/Image/{cloth_type}/{img_number}.{file_type}'

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
               'ImageNumber INT(11) NOT NULL)'
        try:
            cursor.execute(sql)
        except:
            pass

    sql = f'INSERT INTO {cloth_type}List ' \
        '(User, Url, Title, Description, Price, Size, FirstDate, ImageNumber)' \
        f'VALUES("{user_name}", "{url}", "{cloth_title}", "{cloth_description}", "{cloth_price}", "{cloth_size}", "{first_date}", "{img_number}")'
    cursor.execute(sql)

    sql = f'SELECT * FROM {cloth_type}List WHERE ImageNumber = {img_number}'
    cursor.execute(sql)
    db.commit()
    print(cursor.fetchone())

    audioFile.save(f"Data/Image/{cloth_type}/{img_number}.{file_type}")

    return {"message": "제품 등록에 성공하였습니다", "code": 200}, 200