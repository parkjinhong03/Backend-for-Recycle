from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.User.Signup import method

user_space = api.namespace('User', description='APIs for Handling users')

signup_request_post = api.model('Signup_request_post', {
    'name': fields.String,
    'email': fields.String,
    'phone': fields.String,
    'password': fields.String
})

signup_request_put = api.model('Signup_request_put', {
    'password': fields.String,
    'password_check': fields.String
})


@user_space.route('/signup')
class Signup(Resource):
    @api.doc(responses={200: '회원가입 성공',
                        403: '이메일 인증이 되지 않은 계정',
                        410: '입력받은 데이터 중에 공백이 존재함',
                        412: '전화번호 값에 문자열이 포함되어 있음',
                        420: '이미 등록된 이름',
                        421: '이미 등록된 이메일',
                        422: '이미 등록된 전화번호'},
             description='User/signup/email URI로 이메일 인증 후 호출하면 회원가입을 해주는 API로, '
                               '사용자가 메일 인증 전에 회원가입 버튼을 누르면 작동하지 않는다.')
    @api.expect(signup_request_post)
    def post(self):
        return method.post()

    @api.doc(responses={
        200: '비밀번호 재설정 성공',
        401: 'access_token을 headers에 포함하지 않았음',
        422: '잘못된 access_token을 줬음',
        410: '비밀번호와 비밀번호 확인 값이 서로 다름'},
        description='해당 유저에 대한 JWT-token을 받아서 비밀번호를 변경해주는 API')
    @api.expect(signup_request_put)
    @jwt_required
    def put(self):
        return method.put()