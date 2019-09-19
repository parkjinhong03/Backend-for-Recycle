import RequestParser
import smtplib
from email.mime.text import MIMEText
from db_connect import db, cursor
import random


def post():
    '''
    이메일 인증을 위한 POST Method
    :return: status code
    410 - email을 입력하지 않음
    411 - email에 공백이 포함됨
    '''
    email = RequestParser.parser('email')[0]

    if email == None:
        return {"message": "이메일을 입력하지 않음", "code": 410}, 410
    if ' ' in email:
        return {"message": "이메일에 공백이 포함됨", "code": 411}, 411

    num = random.randrange(10000, 100000)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('richimous0719@gmail.com', 'gzuviibjmmxeuoeo')
    msg = MIMEText(f'인증번호: {num}')
    msg['Subject'] = f'confirm your email to signup our Re-cycle service.'
    s.sendmail("richimous0719@gmail.com", email, msg.as_string())
    s.quit()

    sql = f'INSERT INTO emailauth (email, random) VALUES("{email}", {num})'
    cursor.execute(sql)

    return {"message": "이메일을 보냈으니 인증해 주세요", "code": 200}, 200