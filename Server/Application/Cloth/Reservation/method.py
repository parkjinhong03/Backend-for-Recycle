from db_connect import db, cursor
import RequestParser
from flask_jwt_extended import get_jwt_identity

type_to_korea = {
    'Shirts': '상의',
    'Pants': '하의',
    'Shoes': '신발',
    'Accessory': '악세서리'
}


def get():
    _user = get_jwt_identity()
    print(_user)
    return_dict = {}
    count = 1

    sql = f'SELECT * FROM ReservationData WHERE name = "{_user}"'
    cursor.execute(sql)

    for i in cursor.fetchall():
        sql = f'SELECT * FROM {str(i[1]).split("/")[2]}List WHERE url = "{str(i[1])}"'
        cursor.execute(sql)

        data = cursor.fetchone()

        specific_dict = {}

        specific_dict['name'] = data[0]
        specific_dict['type'] = type_to_korea[str(data[1]).split('/')[2]]
        specific_dict['image_url'] = data[1]
        specific_dict['title'] = data[2]
        specific_dict['description'] = data[3]
        specific_dict['price'] = data[4]
        specific_dict['size'] = data[5]
        specific_dict['first_date'] = data[6]
        specific_dict['sell_status'] = data[7]

        return_dict[count] = specific_dict

        count += 1

    return return_dict


def post():

    _user = get_jwt_identity()

    url = str(RequestParser.parser('url')[0])

    if url is None:
        return {"message": "docs에 주어진 대로 모든 params를 전달해 주세요", "code": 410}, 410

    if url.split('/')[0] != 'Cloth' or url.split('/')[1] != 'Image' or url.split('/')[2] not in ['Shirts', 'Shoes', 'Pants', 'Accessory']:
        return {"message": "Cloth/Image/{type}/{filename} 형식의 URL을 주세요", "code": 411}, 411

    sql = f'SELECT * FROM {url.split("/")[2]}List WHERE url = "{url}"'
    cursor.execute(sql)

    if cursor.fetchone() is None:
        return {"message": "해당 사진 URL에 관한 제품 정보가 존재하지 않습니다", "code": 412}, 412

    sql = 'CREATE TABLE ReservationData (' \
          '    name TEXT NOT NULL,' \
          '    url TEXT NOT NULL' \
          ')'
    try:
        cursor.execute(sql)
    except:
        pass

    sql = f'SELECT * FROM ReservationData WHERE name = "{_user}" AND url = "{url}"'
    cursor.execute(sql)
    if cursor.fetchone() is not None:
        return {"message": "이미 예매한 제품입니다.", "code": 413}, 413

    sql = f'INSERT INTO ReservationData (name, url) VALUES("{_user}", "{url}")'
    cursor.execute(sql)
    db.commit()

    return {"message": "제품 찜하기에 성공하였습니다.", "code": 200}, 200