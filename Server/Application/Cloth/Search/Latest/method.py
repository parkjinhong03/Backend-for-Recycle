from db_connect import connect
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

    type_list = ['Shirts', 'Pants', 'Shoes', 'Accessory']

    for i in type_list:
        sql = f'SELECT * FROM {i}List WHERE SellStatus = 0'
        cursor.execute(sql)
        total_data = total_data + list(cursor.fetchall())

    sorted_data = sorted(total_data, key=lambda data: int(data[9]), reverse=True)
    print(sorted_data)

    for count in range(10):
        try:
            _ = sorted_data[count]
        except:
            break

        specific_dict = {}

        specific_dict['name'] = sorted_data[count][0]
        specific_dict['type'] = type_to_korea[str(sorted_data[count][1]).split('/')[2]]
        specific_dict['image_url'] = sorted_data[count][1]
        specific_dict['title'] = sorted_data[count][2]
        specific_dict['description'] = sorted_data[count][3]
        specific_dict['price'] = sorted_data[count][4]
        specific_dict['size'] = sorted_data[count][5]
        specific_dict['first_date'] = sorted_data[count][6]
        specific_dict['status'] = sorted_data[count][10]

        return_dict[count+1] = specific_dict

    db.close()
    return return_dict