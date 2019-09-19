import RequestParser
import smtplib
from email.mime.text import MIMEText
from db_connect import db, cursor
import random


def post2():
    '''
    이메일 인증 완료를 위한 POST Method
    :return: status code
    410 - email에 공백이 포함됨
    411 - number에 공백이 포함되거나 정수형이 아님
    403 - 인증 실패 (인증 번호가 다름)
    200 - 인증 성공
    '''
    email, num = RequestParser.parser('email', 'num')

    sql = f'SELECT random FROM emailauth WHERE email = "{email}"'
    cursor.execute(sql)
    real_num = int(cursor.fetchone()[0])

    if int(num) == real_num:
        return {"messgae": "인증에 성공하였습니다.", "code": 200}, 200
    else:
        return {"messgae": "인증에 실패햐였습니다.", "code": 403}, 403


def post1():
    '''
    이메일 인증 요청을 위한 POST Method
    :return: status code
    410 - email에 공백이 포함됨
    200 - 성공
    '''
    email = RequestParser.parser('email')[0]

    if ' ' in email:
        return {"message": "이메일에 공백이 포함됨", "code": 410}, 410

    num = random.randrange(10000, 100000)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('richimous0719@gmail.com', 'gzuviibjmmxeuoeo')
    msg = MIMEText(f'인증번호: {num}')
    msg['Subject'] = f'confirm your email to signup our Re-cycle service.'
    s.sendmail("richimous0719@gmail.com", email, msg.as_string())
    s.quit()

    sql = f'DELETE FROM emailauth WHERE email = "{email}"'
    cursor.execute(sql)
    sql = f'INSERT INTO emailauth (email, random) VALUES("{email}", {num})'
    cursor.execute(sql)

    return {"message": "이메일을 보냈으니 인증해 주세요", "code": 200}, 200