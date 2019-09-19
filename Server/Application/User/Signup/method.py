from flask_restplus import reqparse
import RequestParser
from db_connect import db, cursor
import hashlib
import smtplib
from email.mime.text import MIMEText


def post():
    '''
    회원가입을 위한 POST Method
    :return: status code
    410 - 공백이 있음
    411 - email이 존재하지 않거나 형식이 잘못됨
    412 - phone 데이터가 정수형이 아니거나 문자열이 존재함
    420 - 이미 등록된 이름
    421 - 이미 등록된 이메일
    422 - 이미 등록된 전화번호
    200 - 성공
    '''

    name, email, phone, password = RequestParser.parser('name', 'email', 'phone', 'password')
    data_list = [name, email, phone, password]

    # 410 예외처리
    for i in data_list:
        if ' ' in i:
            print(i)
            return {"message": "입력 받은 데이터 중 공백이 존재함", "code": 410}, 410

    # 412 예외처리
    try:
        int(phone)
    except ValueError:
        return {"message": "전화번호 값에 문자열이 존재하거나 정수가 아님", "code": 412}, 412

    # 420 예외처리
    sql = f'SELECT * FROM userlog WHERE name = "{name}"'
    cursor.execute(sql)
    data = cursor.fetchone()
    if data:
        return {"message": "이미 존재하는 이름임", "code": 420}, 420

    # 421 예외처리
    sql = f'SELECT * FROM userlog WHERE email = "{email}"'
    cursor.execute(sql)
    data = cursor.fetchone()
    if data:
        return {"message": "이미 존재하는 이메일임", "code": 421}, 421

    # 422 예외처리
    sql = f'SELECT * FROM userlog WHERE phone = "{phone}"'
    cursor.execute(sql)
    data = cursor.fetchone()
    if data:
        return {"message": "이미 존재하는 전화번호임", "code": 422}, 422

    sql = f'INSERT INTO userlog (name, email, phone, password) VALUES("{name}", "{email}", "{phone}", "{password}");'
    cursor.execute(sql)

    return {"message": "회원가입을 성공하였습니다.", "code": 200}, 200 