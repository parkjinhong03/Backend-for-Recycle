from flask_restplus import Resource, fields
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.User.Login import method

login_request = api.model('Login_request', {
    'email': fields.String(required=True, help="Name cannot be blank."),
    'password': fields.String(required=True, help="Name cannot be blank."),
})

login_response = api.model('Login_response', {
    'access_token': fields.String(description="access_token을 발급해서 반환해줌"),
    'refresh_token': fields.String(description="refresh_token 발급해서 반환해줌"),
    'cancel': fields.String(description="해당 유저가 찜한 제품이 뺏겼을 경우, 그 뺏긴 제품에 대한 정보를 가지고 있는 KEY이다.")
})

user_space = api.namespace('User', description='APIs for Handling users')

@user_space.route('/login',
           doc={'description': 'Email과 password 값을 받아서 정보가 일치하다면 JWT-token을 반환해주는 API, 또한 로그인한 계정의 사용자가 찜해논 상품이 뺏겼을 경우, 추가적인 값을 반환해줌.'})
class Login(Resource):
    @api.response(200, '로그인 성공 및 access_token과 refresh_token을 반환해줌.', login_response)
    @api.doc(responses={
        410: 'email 입력 정보에 공백이 있음',
        411: 'password 입력 정보에 공백이 있음',
        420: '존재하지 않는 ID',
        421: '일치하지 않는 PW'
    })
    @api.expect(login_request)
    def post(self):
        return method.post()