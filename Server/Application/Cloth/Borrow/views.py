from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.Cloth.Borrow import method

cloth_namespace = api.namespace('Cloth', description='APIs for Request clothes')

post_parser = api.parser()
post_parser.add_argument('JWT-Token', location='headers', required=True, help='회원 인증을 위해 User/login에서 받은 access_token을 Header에 포함해서 줘야함')
post_parser.add_argument('url', required=True, help='빌릴 제품의 URL을 포함한다.')


@cloth_namespace.route('/Borrow')
class Borrow(Resource):
    @api.doc(
        description='제품을 빌리기 위해 호출하는 API로, JWT-token과 빌릴 제품의 사진 URL를 건네 줘야 한다.',
        responses={
            200: '해당 제품 빌리기 완료',
            410: 'url 값을 주셔야죠!',
            411: 'url을 옳바른 형태로 주지 않음',
            412: '해당 제품이 존재하지 않습니다',
            413: '해당 제품은 빌릴 수 없는 상태입니다',
            414: '해당 유저가 그 등급으로는 이번 달에 더 이상 옷을 빌릴수 없음'
        }
    )
    @api.expect(post_parser)
    @jwt_required
    def post(self):
        return method.post()