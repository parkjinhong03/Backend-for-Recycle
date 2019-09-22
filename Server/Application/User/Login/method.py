from flask_jwt_extended import create_access_token, create_refresh_token
import RequestParser
from db_connect import db, cursor


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

    input_email, input_password = RequestParser.parser('email', 'password')

    if ' ' in input_email:
        return {"message": "Email 값에 공백이 포함되어 있음", "code": 410}, 410
    if ' ' in input_password:
        return {"messsage": "Password 값에 공백이 포함되어 있음", "code": 411}, 411

    sql = f'SELECT password, name FROM userlog WHERE email = "{input_email}"'
    cursor.execute(sql)
    my_log_data = cursor.fetchone()

    try:
        _password = my_log_data[0]
        _name = my_log_data[1]
    except:
        return {"message": "존재하지 않는 ID 입니다.", "code": 420}, 420

    if input_password == _password:
        access_token = create_access_token(identity=_name)
        refresh_token = create_refresh_token(identity=_name)
        return {"message": "로그인에 성공하였습니다.", "access_token": access_token, "refresh_token": refresh_token, "code": 200}, 200
    else:
        return {"message": "일치하지 않는 PW 입니다.", "code": 421}, 421