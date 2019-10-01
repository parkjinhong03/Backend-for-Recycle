from db_connect import db, cursor
import RequestParser

type_to_korea = {
    'Shirts': '상의',
    'Pants': '하의',
    'Shoes': '신발',
    'Accessory': '악세서리'
}


def get(type, img_name):
    type_list = ['Shirts', 'Shoes', 'Pants', 'Accessory']

    if type not in type_list:
        return {"message": "{type} path에 Shirts, Shoes, Pants, Accessory 이외의 값을 줌", "code": 410}, 410

    sql = f'SELECT * FROM {type}List WHERE Url = "Cloth/Image/{type}/{img_name}"'
    cursor.execute(sql)
    cloth_data = cursor.fetchone()

    if cloth_data is None:
        return {"message": "존재하지 않는 상품입니다", "code": 411}, 411

    return_dict = {}

    return_dict['name'] = cloth_data[0]
    return_dict['type'] = type_to_korea[type]
    return_dict['image_url'] = cloth_data[1]
    return_dict['title'] = cloth_data[2]
    return_dict['description'] = cloth_data[3]
    return_dict['price'] = cloth_data[4]
    return_dict['size'] = cloth_data[5]
    return_dict['first_date'] = cloth_data[6]
    return_dict['sell_status'] = cloth_data[7]

    return return_dict