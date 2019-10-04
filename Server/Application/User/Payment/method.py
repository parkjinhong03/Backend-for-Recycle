from db_connect import connect
from flask_jwt_extended import get_jwt_identity
import datetime


def get():
    db, cursor = connect()
    _user = get_jwt_identity()
    return_data = []
    return_dict = {}

    sql = f'SELECT * FROM BorrowData WHERE name = "{_user}"'
    cursor.execute(sql)

    borrow_data = cursor.fetchall()

    for i in borrow_data:
        specific_list = []

        sql = f'SELECT * FROM {str(i[1]).split("/")[2]}List WHERE Url = "{i[1]}"'
        cursor.execute(sql)
        data = cursor.fetchone()

        specific_list.append(data[0]) # 등록자 이름
        specific_list.append(data[1]) # 상품 이미지 URL
        specific_list.append(data[2]) # 상품 이름
        specific_list.append(data[4]) # 상품 가격
        specific_list.append(data[5]) # 상품 사이즈
        specific_list.append(data[9]) # 상품 등록 일자
        specific_list.append(i[5]) # 상품 구매 및 대여 일자
        specific_list.append(i[3]) # 반환 여부
        specific_list.append('대여') # 대여? & 구매?

        now = datetime.datetime.now()
        return_time = datetime.datetime(int(i[2][0:4]), int(i[2][4:6]), int(i[2][6:8]), now.hour, now.minute, now.second)

        return_day = ((now - return_time).days)

        if return_day <= 0:
            specific_list.append(f'{-return_day}일 남음')
        else:
            specific_list.append(f'{return_day}일 지남')

        return_data.append(specific_list)
        specific_list.append(data[10])

    sql = f'SELECT * FROM BuyData WHERE name = "{_user}"'
    cursor.execute(sql)

    buy_data = cursor.fetchall()

    for i in buy_data:
        specific_list = []
        print(i)

        sql = f'SELECT * FROM {str(i[1]).split("/")[2]}List WHERE Url = "{i[1]}"'
        cursor.execute(sql)
        data = cursor.fetchone()

        specific_list.append(data[0]) # 등록자 이름
        specific_list.append(data[1]) # 상품 이미지 URL
        specific_list.append(data[2]) # 상품 이름
        specific_list.append(data[4]) # 상품 가격
        specific_list.append(data[5]) # 상품 사이즈
        specific_list.append(data[9]) # 상품 등록 일자
        specific_list.append(i[2]) # 상품 구매 및 대여 일자
        specific_list.append("") # 반환 여부
        specific_list.append('구매') # 대여? & 구매?
        specific_list.append('')
        specific_list.append(data[10]) # 상품 등록 일자

        return_data.append(specific_list)

    sorted_data = sorted(return_data, key=lambda data: int(data[6]), reverse=True)

    count = 1
    for i in sorted_data:
        specific_dict = {}

        specific_dict['name'] = i[0]
        specific_dict['url'] = i[1]
        specific_dict['title'] = i[2]
        specific_dict['price'] = i[3]
        specific_dict['size'] = i[4]
        specific_dict['register_date'] = i[5]
        specific_dict['deal_date'] = i[6]
        specific_dict['return_status'] = i[7]
        specific_dict['type'] = i[8]
        specific_dict['remain_time'] = i[9]
        specific_dict['status'] = i[10]

        return_dict[count] = specific_dict
        count += 1

    db.close()
    return return_dict