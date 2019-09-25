import RequestParser
from db_connect import db, cursor
from flask import send_file
import random

type_to_korea = {
    'Shirts': '상의',
    'Pants': '하의',
    'Shoes': '신발',
    'Accessory': '악세서리'
}


def get():
    return_dict = {}

    type_list = ['Shirts', 'Pants', 'Shoes', 'Accessory']
    total_data = []

    for i in type_list:
        sql = f'SELECT * FROM {i}List WHERE SellStatus = 0'
        cursor.execute(sql)
        total_data = total_data + list(cursor.fetchall())

    for i in range(10):
        specific_dict = {}
        if not total_data:
            break

        random_data = random.choice(total_data)

        specific_dict['name'] = random_data[0]
        specific_dict['type'] = type_to_korea[str(random_data[1]).split('/')[2]]
        specific_dict['image_url'] = random_data[1]
        specific_dict['title'] = random_data[2]
        specific_dict['description'] = random_data[3]
        specific_dict['price'] = random_data[4]
        specific_dict['size'] = random_data[5]
        specific_dict['first_date'] = random_data[6]

        count = 0
        for j in total_data:
            if j[1] == random_data[1]:
                del total_data[count]
                break
            else:
                count += 1

        return_dict[i+1] = specific_dict

    return return_dict