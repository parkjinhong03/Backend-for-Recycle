from db_connect import connect
import RequestParser
from flask_jwt_extended import get_jwt_identity
import datetime


def delete():
    db, cursor = connect()
    _user = get_jwt_identity()

    url = RequestParser.parser('url')[0]
    if url is None:
        db.close()
        return {"message": "url값을 내놓으란 말이다!!!", "code": 410}, 410

    try:
        sql = f'SELECT * FROM {str(url).split("/")[2]}List WHERE Url = "{url}"'
        cursor.execute(sql)
        cloth_data = cursor.fetchone()
    except:
        db.close()
        return {"message": "url을 옳바른 형태로 건네주세요.", "code": 411}, 411

    if cloth_data is None:
        db.close()
        return {"message": "해당 제품이 존재하지 않습니다.", "code": 412}, 412

    sql = f'SELECT * FROM BorrowData WHERE name = "{_user}" AND url = "{url}"'
    cursor.execute(sql)
    borrow_data = cursor.fetchone()
    print(borrow_data)

    if borrow_data is None:
        db.close()
        return {"message": "해당 제품을 빌린 적이 없습니다", "code": 413}, 413

    sql = f'UPDATE BorrowData SET ReturnStatus = 1 WHERE url = "{url}"'
    cursor.execute(sql)
    db.commit()

    sql = f'UPDATE {str(url).split("/")[2]}List SET SellStatus = 0 WHERE Url = "{url}"'
    cursor.execute(sql)
    db.commit()

    db.close()
    return {"message": "해당 제품 반납 성공", "code": 200}, 200


def post():
    db, cursor = connect()
    sql = 'CREATE TABLE BorrowData (' \
          '    name TEXT NOT NULL,' \
          '    url TEXT NOT NULL,' \
          '    deadline TEXT NOT NULL,' \
          '    ReturnStatus TEXT NOT NULL,' \
          '    BuyStatus TEXT NOT NULL,' \
          '    date TEXT NOT NULL' \
          ')'
    try:
        cursor.execute(sql)
        db.commit()
    except:
        pass

    _user = get_jwt_identity()

    url = RequestParser.parser('url')[0]

    if url is None:
        db.close()
        return {"message": "url값을 내놓으란 말이다!!!", "code": 410}, 410


    try:
        sql = f'SELECT * FROM {str(url).split("/")[2]}List WHERE Url = "{url}"'
        cursor.execute(sql)
        cloth_data = cursor.fetchone()
    except:
        db.close()
        return {"message": "url을 옳바른 형태로 건네주세요.", "code": 411}, 411

    if cloth_data is None:
        db.close()
        return {"message": "해당 제품이 존재하지 않습니다.", "code": 412}, 412

    if int(cloth_data[7]) != 0:
        db.close()
        return {"message": "해당 제품을 빌릴 수 없는 상태입니다.", "code": 413}, 413

    sql = f'SELECT * FROM UserRank'
    cursor.execute(sql)
    user_rank = cursor.fetchone()[1]

    rank_number = {
        'Normal': 5,
        'VIP': 10,
        'VVIP': 20
    }
    now = datetime.datetime.now()
    month = now.strftime("%Y%m")

    sql = f'SELECT * FROM BorrowData WHERE name = "{_user}"'
    cursor.execute(sql)
    borrow_count = 0

    borrow_data = cursor.fetchall()

    for i in borrow_data:
        if i[5][0:6] == month:
            borrow_count += 1

    print(borrow_count)
    print(rank_number[user_rank])

    if borrow_count >= rank_number[user_rank]:
        db.close()
        return {"message": "해당 회원이 이번 달에 빌릴수 있는 옷의 갯수가 초과되었습니다.", "code": 414}, 414

    if int(now.month) <= 8:
        deadline_date = str(now.year) + '0' + str(int(now.month) + 1)
    elif int(now.month) > 8 and int(now.month) < 11:
        deadline_date = str(now.year) + str(int(now.month) + 1)
    else:
        deadline_date = str(int(now.year) + 1) + '01'

    deadline_date = deadline_date + str(now.day)
    print(deadline_date)
    print(now.strftime("%Y%m%d%H%M%S"))

    sql = f'INSERT INTO BorrowData (name, url, deadline, ReturnStatus, BuyStatus, date) VALUES("{_user}", "{url}", "{deadline_date}", "0", "0", {now.strftime("%Y%m%d%H%M%S")})'
    cursor.execute(sql)
    db.commit()

    sql = f'UPDATE {str(url).split("/")[2]}List SET SellStatus = 1 WHERE Url = "{url}"'
    cursor.execute(sql)
    db.commit()

    sql = f'SELECT * FROM ReservationData WHERE url = "{url}"'
    cursor.execute(sql)
    cancle_data = list(cursor.fetchall())

    for i in cancle_data:
        sql = f'INSERT INTO ReservationCancelData (name, url, register_name, register_title) VALUES("{i[0]}", "{i[1]}", "{i[2]}", "{i[3]}")'
        cursor.execute(sql)
        db.commit()

    sql = f'DELETE FROM ReservationData WHERE url = "{url}"'
    cursor.execute(sql)
    db.commit()

    db.close()
    return {"message": "해당 유저 아이디로 옷 빌려 입어보기 신청 완료", "code": 200}, 200