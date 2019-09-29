from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.User.Rank import method

cloth_namespace = api.namespace('User', description='APIs for Request users')

put_parser = api.parser()
put_parser.add_argument('JWT-Token', location='headers', required=True, help='회원 인증을 위해 User/login에서 받은 access_token을 Header에 포함해서 줘야함')
put_parser.add_argument('rank', required=True, help='Normal, VIP, VVIP 중에서 원하는 등급')


@cloth_namespace.route('/Rank')
class Rank(Resource):
    @api.doc(
        description='해당 유저의 등급(Normal, VIP, VVIP)을 변경하기 위해 호출하는 API로, JWT-token을 포함해서 호출해야 한다.',
        responses={
            200: '등급 변경 요청 완료',
            410: 'docs에 나온데로 params을 달라!',
            411: 'rank의 VALUE 값으로 [Normal, VIP, VVIP]만을 주세요',
            412: '이미 해당 요청 등급과 같은 등급임'
        }
    )
    @api.expect(put_parser)
    @jwt_required
    def put(self):
        return method.put()