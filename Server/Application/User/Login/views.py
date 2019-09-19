from flask_restplus import Resource
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.User.Login import method


@api.route('/User/login',
           doc={'description': 'Email과 password 값을 받아서 정보가 일치하다면 JWT-token을 반환해주는 API'})
@api.doc(
    params={
        'email': 'An Email',
        'password': 'Your password'
    }
)
class Login(Resource):
    @api.doc(responses={
        200: '로그인 성공 및 JWT token 반환',
        410: 'email 입력 정보에 공백이 있음',
        411: 'password 입력 정보에 공백이 있음',
        420: '존재하지 않는 ID',
        421: '일치하지 않는 PW'
    })
    def post(self):
        return method.post()