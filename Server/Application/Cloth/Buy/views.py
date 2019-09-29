from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.Cloth.Buy import method

cloth_namespace = api.namespace('Cloth', description='APIs for Request clothes')

post_parser = api.parser()
post_parser.add_argument('JWT-Token', location='headers', required=True, help='회원 인증을 위해 User/login에서 받은 access_token을 Header에 포함해서 줘야함')
post_parser.add_argument('url', required=True, help='구매할 제품의 URL을 포함한다.')


@cloth_namespace.route('/Buy')
class Buy(Resource):
    @api.doc(
        description='해당 제품을 구매할 때 호출하는 API로, JWT-token과 구매하려는 제품의 이미지 URL을 보내면 된다.',
        responses={
            200: '해당 제품 구매 성공',
            410: 'url 값을 주셔야죠!',
            411: 'url을 옳바른 형태로 주지 않음',
            412: '해당 제품이 존재하지 않습니다',
            413: '해당 제품은 구매할 수 없는 상태입니다',
        }
    )
    @api.expect(post_parser)
    @jwt_required
    def post(self):
        return method.post()