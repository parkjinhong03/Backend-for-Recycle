from db_connect import db, cursor
import random


def get(cloth_type):
    return_dict = {}
    count = 1

    type_list = ['Shirts', 'Shoes', 'Pants', 'Accessory']
    if cloth_type not in type_list:
        return {"message": "{type} path에 Shirts, Shoes, Pants, Accessory 이외의 값을 줌", "code": 410}, 410

    sql = f'SELECT * FROM {cloth_type}List WHERE SellStatus = 0'
    cursor.execute(sql)
    total_data = list(cursor.fetchall())

    index_list = []
    random_list = []

    for data in total_data:
        index_list.append(data[8])

    while True:
        if not index_list:
            break
        random_data = random.choice(index_list)
        random_list.append(random_data)
        index_list.remove(random_data)

    for term in range((len(random_list)-1) // 5 + 1):
        return_middle_dict = {}
        for index in random_list[term*5:term*5+5]:
            specific_dict = {}
            data_list = []

            for i in total_data:
                if i[8] == index:
                    data_list = i
                    del i
                    break

            specific_dict['name'] = data_list[0]
            specific_dict['image_url'] = data_list[1]
            specific_dict['title'] = data_list[2]
            specific_dict['description'] = data_list[3]
            specific_dict['price'] = data_list[4]
            specific_dict['size'] = data_list[5]
            specific_dict['first_date'] = data_list[6]

            return_middle_dict[count] = specific_dict
            count += 1

        return_dict[term+1] = return_middle_dict
        count = 1

    return return_dict