from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_refresh_token_required
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.User.Login.Refresh import method

refresh_response = api.model('Refresh_response', {
    'access_token': fields.String(required=True, help="Name cannot be blank.")
})

parser = api.parser()
parser.add_argument('refresh_token', location='headers')

user_space = api.namespace('User', description='APIs for Handling users')

@user_space.route('/login/refresh',
                  doc={'description': '만약 access_token의 만료일이 다 되었으면 refresh_token을 header에 넣어서 이 API를 호출해서, 새로운 access_token을 발급받을 수 있다.'})
class Refresh(Resource):
    @api.response(200, 'refresh_token 인증 성공 및 새 access_token 발급', refresh_response)
    @api.doc(responses={
        401: 'refresg_token의 값이 header에 포함되지 않았음',
        422: 'refresh_token의 값이 외부 요인에 의해 변형됨',
    })
    @api.expect(parser)
    @jwt_refresh_token_required
    def post(self):
        return method.post()