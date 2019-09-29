from db_connect import cursor, db
import RequestParser
from flask_jwt_extended import get_jwt_identity
import datetime


def post():
    sql = 'CREATE TABLE BuyData (' \
          '    name TEXT NOT NULL,' \
          '    url TEXT NOT NULL,' \
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
        return {"message": "url값을 내놓으란 말이다!!!", "code": 410}, 410

    try:
        sql = f'SELECT * FROM {str(url).split("/")[2]}List WHERE Url = "{url}"'
        cursor.execute(sql)
        cloth_data = cursor.fetchone()
    except:
        return {"message": "url을 옳바른 형태로 건네주세요.", "code": 411}, 411

    if cloth_data is None:
        return {"message": "해당 제품이 존재하지 않습니다.", "code": 412}, 412

    if int(cloth_data[7]) != 0:
        if int(cloth_data[7]) == 2:
            return {"message": "해당 제품은 구매할 수 없는 상태입니다.", "code": 413}, 413
        else:
            sql = f'SELECT * FROM BorrowData WHERE url = "{url}" AND name = "{_user}"'
            cursor.execute(sql)

            if cursor.fetchone() is None:
                return {"message": "해당 제품은 구매할 수 없는 상태입니다.", "code": 413}, 413

    now = datetime.datetime.now()

    sql = f'INSERT INTO BuyData (name, url, date) VALUES("{_user}", "{url}", "{now.strftime("%Y%m%d%H%M%S")}")'
    cursor.execute(sql)
    db.commit()

    sql = f'UPDATE {str(url).split("/")[2]}List SET SellStatus = 2 WHERE Url = "{url}"'
    cursor.execute(sql)
    db.commit()

    sql = f'SELECT * FROM BorrowData WHERE url = "{url}" AND name = "{_user}"'
    cursor.execute(sql)

    if cursor.fetchone() is not None:
        sql = f'DELETE FROM BorrowData WHERE url = "{url}"'
        cursor.execute(sql)
        db.commit()

    return {"message": "해당 제품 구매 성공", "code": 200}, 200