from flask_jwt_extended import create_access_token, create_refresh_token
import RequestParser
from db_connect import connect


def post():
    '''
    로그인을 위한 POST Method
    :return: status code
    410 - email 입력 정보에 공백이 있음
    411 - password 입력 정보에 공백이 있음
    420 - 존재하지 않는 ID
    421 - 일치하지 않는 PW
    200 - 로그인 성공 및 JWT token 반환
    '''

    db, cursor = connect()
    input_email, input_password = RequestParser.parser('email', 'password')

    if ' ' in input_email:
        db.close()
        return {"message": "Email 값에 공백이 포함되어 있음", "code": 410}, 410
    if ' ' in input_password:
        db.close()
        return {"messsage": "Password 값에 공백이 포함되어 있음", "code": 411}, 411

    sql = f'SELECT password, name FROM userlog WHERE email = "{input_email}"'
    cursor.execute(sql)
    my_log_data = cursor.fetchone()

    try:
        _password = my_log_data[0]
        _name = my_log_data[1]
    except:
        db.close()
        return {"message": "존재하지 않는 ID 입니다.", "code": 420}, 420

    if input_password != _password:
        db.close()
        return {"message": "일치하지 않는 PW 입니다.", "code": 421}, 421

    access_token = create_access_token(identity=_name)
    refresh_token = create_refresh_token(identity=_name)

    sql = 'CREATE TABLE ReservationCancelData (' \
          '    name TEXT NOT NULL,' \
          '    url TEXT NOT NULL,' \
          '    register_name TEXT NOT NULL,' \
          '    register_title TEXT NOT NULL' \
          ')'
    try:
        cursor.execute(sql)
    except:
        pass

    sql = f'SELECT * FROM ReservationCancelData WHERE name = "{_name}"'
    cursor.execute(sql)
    cancel_data = list(cursor.fetchall())
    cancel_dict = {}
    count = 1

    for i in cancel_data:
        specific_dict = {}

        specific_dict['name'] = i[2]
        specific_dict['title'] = i[3]

        cancel_dict[count] = specific_dict
        count += 1

    sql = f'DELETE FROM ReservationCancelData WHERE name = "{_name}"'
    cursor.execute(sql)
    db.commit()

    sql = 'CREATE TABLE UserImage (' \
          '    name TEXT NOT NULL,' \
          '    url TEXT NOT NULL' \
          ')'
    try:
        cursor.execute(sql)
        db.commit()
    except:
        pass

    sql = f'SELECT * FROM UserImage WHERE name = "{_name}"'
    cursor.execute(sql)

    if cursor.fetchone() is None:
        sql = f'INSERT INTO UserImage (name, url) VALUES("{_name}", "User/Profile/default.jpg")'
        cursor.execute(sql)
        db.commit()

    sql = 'CREATE TABLE UserRank (' \
          '    name TEXT NOT NULL,' \
          '    rank TEXT NOT NULL' \
          ')'
    try:
        cursor.execute(sql)
        db.commit()
    except:
        pass

    sql = f'SELECT * FROM UserRank WHERE name = "{_name}"'
    cursor.execute(sql)

    if cursor.fetchone() is None:
        sql = f'INSERT INTO UserRank (name, rank) VALUES("{_name}", "Normal")'
        cursor.execute(sql)
        db.commit()

    db.close()
    return {"message": "로그인에 성공하였습니다.", "access_token": access_token, "refresh_token": refresh_token, "code": 200, "cancle": cancel_dict}, 200