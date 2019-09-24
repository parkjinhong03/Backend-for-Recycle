from db_connect import db, cursor


def get(cloth_type):
    return_dict = {}
    count = 1

    type_list = ['Shirts', 'Shoes', 'Pants', 'Accessory']
    if cloth_type not in type_list:
        return {"message": "{type} path에 Shirts, Shoes, Pants, Accessory 이외의 값을 줌", "code": 410}, 410

    sql = f'SELECT * FROM {cloth_type}List WHERE SellStatus = 0'
    cursor.execute(sql)
    total_data = cursor.fetchall()

    for data in total_data:
        specific_dict = {}

        specific_dict['name'] = data[0]
        specific_dict['image_url'] = data[1]
        specific_dict['title'] = data[2]
        specific_dict['description'] = data[3]
        specific_dict['price'] = data[4]
        specific_dict['size'] = data[5]
        specific_dict['first_date'] = data[6]

        return_dict[count] = specific_dict
        count += 1

    return return_dict