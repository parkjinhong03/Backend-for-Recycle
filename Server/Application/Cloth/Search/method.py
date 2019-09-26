from db_connect import db, cursor

type_to_korea = {
    'Shirts': '상의',
    'Pants': '하의',
    'Shoes': '신발',
    'Accessory': '악세서리'
}


def get(input):
    return_dict = {}
    total_data = []
    count = 1

    type_list = ['Shirts', 'Pants', 'Shoes', 'Accessory']

    for i in type_list:
        sql = f'SELECT * FROM {i}List'
        cursor.execute(sql)
        total_data = total_data + list(cursor.fetchall())

    for i in total_data:
        if input in i[2] or input in i[3]:
            specific_dict = {}

            specific_dict['name'] = i[0]
            specific_dict['type'] = type_to_korea[str(i[1]).split('/')[2]]
            specific_dict['image_url'] = i[1]
            specific_dict['title'] = i[2]
            specific_dict['description'] = i[3]
            specific_dict['price'] = i[4]
            specific_dict['size'] = i[5]
            specific_dict['first_date'] = i[6]

            return_dict[count] = specific_dict
            count += 1

    return return_dict