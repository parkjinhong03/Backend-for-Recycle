from db_connect import connect
import RequestParser
from flask_jwt_extended import get_jwt_identity

type_to_korea = {
    'Shirts': '상의',
    'Pants': '하의',
    'Shoes': '신발',
    'Accessory': '악세서리'
}


def delete():
    db, cursor = connect()
    _user = get_jwt_identity()

    url = str(RequestParser.parser('url')[0])

    if url is None:
        db.close()
        return {"message": "docs에 주어진 대로 모든 params를 전달해 주세요", "code": 410}, 410

    if url.split('/')[0] != 'Cloth' or url.split('/')[1] != 'Image' or url.split('/')[2] not in ['Shirts', 'Shoes', 'Pants', 'Accessory']:
        db.close()
        return {"message": "Cloth/Image/{type}/{filename} 형식의 URL을 주세요", "code": 411}, 411

    sql = f'SELECT * FROM BasketData WHERE url = "{url}" AND name = "{_user}"'
    cursor.execute(sql)
    delete_data = cursor.fetchone()

    if delete_data is None:
        db.close()
        return {"message": "해당 제품을 장바구니에 담지 않았습니다.", "code": 412}, 412

    sql = f'DELETE FROM BasketData WHERE name = "{_user}" AND url = "{url}"'
    cursor.execute(sql)
    db.commit()

    db.close()
    return {"message": "제품 장바구니에서 꺼내기 완료", "code": 200}, 200


def get():
    db, cursor = connect()
    _user = get_jwt_identity()
    print(_user)
    return_dict = {}
    count = 1

    sql = f'SELECT * FROM BasketData WHERE name = "{_user}"'
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
        specific_dict['status'] = data[10]

        return_dict[count] = specific_dict

        count += 1

    db.close()
    return return_dict


def post():
    db, cursor = connect()
    _user = get_jwt_identity()

    url = str(RequestParser.parser('url')[0])

    if url is None:
        db.close()
        return {"message": "docs에 주어진 대로 모든 params를 전달해 주세요", "code": 410}, 410

    if url.split('/')[0] != 'Cloth' or url.split('/')[1] != 'Image' or url.split('/')[2] not in ['Shirts', 'Shoes', 'Pants', 'Accessory']:
        db.close()
        return {"message": "Cloth/Image/{type}/{filename} 형식의 URL을 주세요", "code": 411}, 411

    sql = f'SELECT * FROM {url.split("/")[2]}List WHERE url = "{url}"'
    cursor.execute(sql)

    if cursor.fetchone() is None:
        db.close()
        return {"message": "해당 사진 URL에 관한 제품 정보가 존재하지 않습니다", "code": 412}, 412

    sql = 'CREATE TABLE BasketData (' \
          '    name TEXT NOT NULL,' \
          '    url TEXT NOT NULL' \
          ')'
    try:
        cursor.execute(sql)
    except:
        pass

    sql = f'SELECT * FROM BasketData WHERE name = "{_user}" AND url = "{url}"'
    cursor.execute(sql)
    if cursor.fetchone() is not None:
        db.close()
        return {"message": "이미 장바구니에 담은 제품입니다.", "code": 413}, 413

    sql = f'INSERT INTO BasketData (name, url) VALUES("{_user}", "{url}")'
    cursor.execute(sql)
    db.commit()

    db.close()
    return {"message": "해당 제품을 장바구니 담기에 성공하였습니다.", "code": 200}, 200