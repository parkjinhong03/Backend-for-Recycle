from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.User.Payment import method

user_namespace = api.namespace('User', description='APIs for Request users')

get_parser = api.parser()
get_parser.add_argument('JWT-Token', location='headers', required=True, help='회원 인증을 위해 User/login에서 받은 access_token을 Header에 포함해서 줘야함')


@user_namespace.route('/Payment')
class Payment(Resource):
    @api.doc(
        description='해당 회원의 결제 내역을 반환해주는 API로, JWT-token을 건네 줘야 한다.',
        responses={
            200: '결제 내역 반환 성공'
        }
    )
    @api.expect(get_parser)
    @jwt_required
    def get(self):
        return method.get()