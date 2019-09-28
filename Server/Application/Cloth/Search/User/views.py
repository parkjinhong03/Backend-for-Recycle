from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.Cloth.Search.User import method

cloth_namespace = api.namespace('Cloth', description='APIs for Request clothes')

get_parser = api.parser()
get_parser.add_argument('JWT-Token', location='headers', required=True, help='회원 인증을 위해 User/login에서 받은 access_token을 Header에 포함해서 줘야함')


@cloth_namespace.route('/My')
class MyCloth(Resource):
    @api.doc(
        description='JWT-token을 받아서 해당 유저가 등록한 옷에 대한 정보를 반환하는 API',
        responses={
            200: '데이터 반환 성공',
            410: '해당 유저가 존재하지 않음'
        }
    )
    @api.expect(get_parser)
    @jwt_required
    def get(self):
        return method.get()