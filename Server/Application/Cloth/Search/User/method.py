from db_connect import connect
from flask_jwt_extended import get_jwt_identity

type_to_korea = {
    'Shirts': '상의',
    'Pants': '하의',
    'Shoes': '신발',
    'Accessory': '악세서리'
}


def get():
    db, cursor = connect()
    return_dict = {}
    total_data = []
    _user = get_jwt_identity()
    number_count = 1

    sql = f'SELECT * FROM userlog WHERE name = "{_user}"'
    cursor.execute(sql)

    if cursor.fetchone() is None:
        db.close()
        return {"message": "해당 유저가 존재하지 않습니다.", "code": 410}, 410

    type_list = ['Shirts', 'Pants', 'Shoes', 'Accessory']

    for i in type_list:
        sql = f'SELECT * FROM {i}List WHERE User = "{_user}"'
        cursor.execute(sql)
        total_data = total_data + list(cursor.fetchall())

    for count in total_data:
        specific_dict = {}

        specific_dict['name'] = count[0]
        specific_dict['type'] = type_to_korea[str(count[1]).split('/')[2]]
        specific_dict['image_url'] = count[1]
        specific_dict['title'] = count[2]
        specific_dict['description'] = count[3]
        specific_dict['price'] = count[4]
        specific_dict['size'] = count[5]
        specific_dict['first_date'] = count[6]
        specific_dict['sell_status'] = count[7]
        specific_dict['status'] = count[10]

        return_dict[number_count] = specific_dict
        number_count += 1

    db.close()
    return return_dict