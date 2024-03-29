from flask_restplus import reqparse
from flask_jwt_extended import get_jwt_identity
import RequestParser
from db_connect import connect
import hashlib
import smtplib
from email.mime.text import MIMEText


def put():
    '''
    비밀번호 변경을 위한 PUT Method
    :return: status code
    401 - access_token을 headers에 포함하지 않았음
    410 - 비밀번호 값이 서로 다름
    422 - 잘못된 access_token을 줬음
    200 - 성공
    '''
    db, cursor = connect()
    _userName = get_jwt_identity()
    print(_userName)

    password, password_check = RequestParser.parser('password', 'password_check')
    print(password, password_check)

    if password_check != password:
        db.close()
        return {"message": "비밀번호와 비밀번호 확인 값이 서로 다름", "code": 410}, 410

    sql = f'UPDATE userlog SET password = "{password}" WHERE name = "{_userName}"'
    cursor.execute(sql)

    db.close()
    return {"message": "비밀번호 변경 성공", "code": 200}, 200


def post():
    '''
    회원가입을 위한 POST Method
    :return: status code
    403 - 이메일 인증이 되지 않은 상태임
    410 - 공백이 있음
    411 - email이 존재하지 않거나 형식이 잘못됨
    412 - phone 데이터에 문자열이 존재하거나 형식이 잘못됨
    420 - 이미 등록된 이름
    421 - 이미 등록된 이메일
    422 - 이미 등록된 전화번호
    200 - 성공
    '''

    db, cursor = connect()
    sql1 = "CREATE TABLE userlog (" \
           "     name TEXT NOT NULL," \
           "     email TEXT NOT NULL," \
           "     phone TEXT NOT NULL," \
           "     password TEXT NOT NULL" \
           ")"

    sql2 = "CREATE TABLE emailauth  (" \
           "     email TEXT NOT NULL," \
           "     random INT(11) NOT NULL," \
           "     AuthStatus BINARY(1) NOT NULL DEFAULT 0" \
           ")"
    try:
        cursor.execute(sql1)
    except:
        pass

    try:
        cursor.execute(sql2)
    except:
        pass

    name, email, phone, password = RequestParser.parser('name', 'email', 'phone', 'password')
    data_list = [name, email, phone, password]

    # 410 예외처리
    for i in data_list:
        if ' ' in i:
            db.close()
            return {"message": "입력 받은 데이터 중 공백이 존재함", "code": 410}, 410

    # 412 예외처리
    try:
        int(phone)
    except ValueError:
        db.close()
        return {"message": "전화번호 값에 문자열이 존재하거나 형식이 잘못됨", "code": 412}, 412

    if len(str(phone)) != 11:
        db.close()
        return {"message": "전화번호 값에 문자열이 존재하거나 형식이 잘못됨", "code": 412}, 412

    # 420 예외처리
    sql = f'SELECT * FROM userlog WHERE name = "{name}"'
    cursor.execute(sql)
    data = cursor.fetchone()
    if data:
        db.close()
        return {"message": "이미 존재하는 이름임", "code": 420}, 420

    # 421 예외처리
    sql = f'SELECT * FROM userlog WHERE email = "{email}"'
    cursor.execute(sql)
    data = cursor.fetchone()
    if data:
        db.close()
        return {"message": "이미 존재하는 이메일임", "code": 421}, 421

    # 422 예외처리
    sql = f'SELECT * FROM userlog WHERE phone = "{phone}"'
    cursor.execute(sql)
    data = cursor.fetchone()
    if data:
        db.close()
        return {"message": "이미 존재하는 전화번호임", "code": 422}, 422

    sql = f'SELECT * FROM emailauth WHERE email = "{email}"'
    cursor.execute(sql)
    AuthData = cursor.fetchone()

    if AuthData == None:
        db.close()
        return {"message": "이메일 인증을 완료하지 않은 상태임", "code": 403}, 403

    status_code = int(AuthData[2])

    if status_code == 0:
        db.close()
        return {"message": "이메일 인증을 완료하지 않은 상태임", "code": 403}, 403


    sql = f'INSERT INTO userlog (name, email, phone, password) VALUES("{name}", "{email}", "{phone}", "{password}");'
    cursor.execute(sql)

    db.close()
    return {"message": "회원가입을 성공하였습니다.", "code": 200}, 200