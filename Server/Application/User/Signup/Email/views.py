from flask_restplus import Resource, fields
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.User.Signup.Email import method

user_space = api.namespace('User', description='APIs for Handling users')

email_request = api.model('Email_request', {
    'email': fields.String
})

@user_space.route('/email',
           doc={'description': '사용자가 인증 번호 발급 버튼을 눌렀을 때 호출하는 APi로, 인증을 위해 email 주소를 넘겨 받아 실제로 그 email 주소로 인증 번호를 발송해주는 API (Gmail 밖에 안됨)'})
class Email(Resource):
    @api.doc(responses={
        200: '인증번호 발송 성공',
        410: 'Email 값에 공백이 포함됨'
    })
    @api.expect(email_request)
    def post(self):
        return method.post1()

@user_space.route('/email/auth',
           doc={'description': '사용자가 인증 번호 발급 및 입력 후 확인 버튼을 눌렀을 때 호출하는 API로, 인증 번호를 제대로 썼다면 그 이메일에 대한 인증을 완료해주는 API 이다.'})
@api.doc(params={
    'email': 'An Email address',
    'num': 'Email authentication number'
})
class EmailAuth(Resource):
    @api.doc(responses={
        200: '해당 Email 인증 성공',
        403: '인증 번호가 달라서 인증에 실패함',
        410: 'Email 값에 공백이 포함됨',
        411: 'number에 공백이 포함되거나 문자열이 포함되어 있음'
    })
    def post(self):
        return method.post2()