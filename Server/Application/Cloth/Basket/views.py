from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.Cloth.Basket import method

cloth_namespace = api.namespace('Cloth', description='APIs for Request clothes')

post_parser = api.parser()
post_parser.add_argument('JWT-Token', location='headers', required=True, help='회원 인증을 위해 User/login에서 받은 access_token을 Header에 포함해서 줘야함')
post_parser.add_argument('url', required=True, help='장바구니에 담으려는 제품의 Image URL 값을 전달 해야한다.')

get_parser = api.parser()
get_parser.add_argument('JWT-Token', location='headers', required=True, help='회원 인증을 위해 User/login에서 받은 access_token을 Header에 포함해서 줘야함')

delete_parser = api.parser()
delete_parser.add_argument('JWT-Token', location='headers', required=True, help='회원 인증을 위해 User/login에서 받은 access_token을 Header에 포함해서 줘야함')
delete_parser.add_argument('url', required=True, help='장바구니에서 꺼내려는 제품의 Image URL 값을 전달 해야한다.')


@cloth_namespace.route('/Basket')
class Basket(Resource):
    @api.doc(
        description="제품을 내 장바구니에 등록하기 위한 API로, JWT-token과 장바구니에 담을 제품의 사진 URL을 주면 성공한다.",
        responses={
            200: '제품 장바구니에 담기 성공',
            410: 'docs에 나와있는 모든 params를 전달하지 않음',
            411: 'Cloth/Image/{type}/{filename} 형식의 URL로 주지 않음.',
            412: '존재하지 않는 제품의 사진 URL임',
            413: '이미 장바구니에 넣은 제품임'
        }
    )
    @api.expect(post_parser)
    @jwt_required
    def post(self):
        return method.post()

    @api.doc(
        description='해당 유저가 장바구니에 담은 제품을 반환해주는 API로, 그 유저에 대한 JWT-token을 건네 줘야 한다.',
        responses={
            200: '장바구니에 담은 제품들 반환 성공'
        }
    )
    @api.expect(get_parser)
    @jwt_required
    def get(self):
        return method.get()

    @api.doc(
        description='해당 유저가 장바구니에 담은 제품을 꺼낼 떄 사용하는 API로, JWT-token과 꺼낼 제품의 사진 URL을 주면 성공한다.',
        responses={
            200: '제품 장바구니에서 꺼내기 완료',
            410: 'docs에 나와있는 모든 params를 전달하지 않음',
            411: 'Cloth/Image/{type}/{filename} 형식의 URL로 주지 않음.',
            412: '해당 유저가 장바구니에 담지 않은 제품임'
        }
    )
    @api.expect(delete_parser)
    @jwt_required
    def delete(self):
        return method.delete()