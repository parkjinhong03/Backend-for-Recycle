from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.User.Signup import method

user_space = api.namespace('User', description='APIs for Handling users')

signup_request = api.model('Signup_request', {
    'name': fields.String,
    'email': fields.String,
    'phone': fields.String,
    'password': fields.String
})

@user_space.route('/signup', doc={'description': 'User/signup/email URI로 이메일 인증 후 호출하면 회원가입을 해주는 API로, '
                               '사용자가 메일 인증 전에 회원가입 버튼을 누르면 작동하지 않는다.'})
class Signup(Resource):
    @api.doc(responses={200: '회원가입 성공',
                        403: '이메일 인증이 되지 않은 계정',
                        410: '입력받은 데이터 중에 공백이 존재함',
                        412: '전화번호 값에 문자열이 포함되어 있음',
                        420: '이미 등록된 이름',
                        421: '이미 등록된 이메일',
                        422: '이미 등록된 전화번호'})
    @api.expect(signup_request)
    def post(self):
        return method.post()

    @jwt_required
    def put(self):
        return method.put()