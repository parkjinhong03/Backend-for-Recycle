import RequestParser
from db_connect import db, cursor
from flask import request
from werkzeug import security
from flask_restplus import reqparse
import werkzeug


def post(cloth_type):
    '''
    옷을 등록하주는 POST Method
    :return: status code
    410 - {type} path에 Shirts, Shoes, Pants, Accessory 이외의 값을 줌
    411 - 전달한 파일의 확장자가 jpg, png 외의 파일임
    '''

    type_list = ['Shirts', 'Shoes', 'Pants', 'Accessory']
    if cloth_type not in type_list:
        return {"message": "{type} path에 Shirts, Shoes, Pants, Accessory 이외의 값을 줌", "code": 410}, 410

    cloth_description, cloth_price, cloth_size = RequestParser.parser('description', 'price', 'size')
    print(cloth_type, cloth_description, cloth_price, cloth_size)

    parse = reqparse.RequestParser()
    parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
    args = parse.parse_args()
    audioFile = args['file']

    file_type = audioFile.filename.split('.')[1]

    print(type(file_type))

    file_type_list = ['jpg', 'png']
    if file_type not in file_type_list:
        return {"message": "jpg 또는 png 확장자를 가진 파일을 보내지 않음", "code": 411}, 411


    # url = f'Cloth/Image/{cloth_type}/{}'

    # audioFile.save(f"Data/Image/{cloth_type}/12341.{file_type}")

    return f'{cloth_type}'