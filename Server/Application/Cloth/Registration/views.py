from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.Cloth.Registration import method

cloth_namespace = api.namespace('Cloth', description='APIs for Request clothes')

post_parser = api.parser()
post_parser.add_argument('JWT-Token', location='headers', required=True, help='회원 인증을 위해 User/login에서 받은 access_token을 Header에 포함해서 줘야함')
post_parser.add_argument('title', type=str, required=True, help='등록할 옷의 이름')
post_parser.add_argument('description', type=str, required=True, help='등록할 옷에 대한 추가 정보')
post_parser.add_argument('price', type=int,  required=True, help='등록할 옷의 가격에 대한 정보')
post_parser.add_argument('size', type=str, required=True, help='등록할 옷의 사이즈에 대한 정보')
post_parser.add_argument('first_date', type=int, required=True, help='등록할 옷을 처음으로 구매한 날짜(YYYYMMDD 형식으로 주게 하기 바람)')
post_parser.add_argument('cloth_type', location='path', required=True, help='Cloth/Register/뒤의 경로에 넣는 값으로, Shirts, Shoes, Pants, Accessory 를 넣을 수 있다.')
post_parser.add_argument('binary', type=str, required=True, help='등록할 이미지의 BASE64 인코딩 데이터를 건네줘야 한다.')

delete_parser = api.parser()
delete_parser.add_argument('JWT-Token', location='headers', required=True, help='회원 인증을 위해 User/login에서 받은 access_token을 Header에 포함해서 줘야함')
delete_parser.add_argument('url', required=True, help='삭제하려는 제품의 Image URL 값을 전달 해야한다.')
delete_parser.add_argument('cloth_type', location='path', required=True, help='Cloth/Register/뒤의 경로에 넣는 값으로, Shirts, Shoes, Pants, Accessory 를 넣을 수 있다.')


@cloth_namespace.route('/Register/<string:cloth_type>')
class Register(Resource):
    @api.doc(
        description='중고로 거래할 제품을 등록해주는 API로, {type}에 Shirts, Shoes, Pants, Accessory 를 넣을 수 있다.',
        responses={
            200: '제품 등록 성공',
            410: '{type} path에 Shirts, Shoes, Pants, Accessory 이외의 값을 줌',
            411: '전달한 파일의 확장자가 jpg, png 외의 파일임',
            412: 'price 값에 문자열이 포함되어있음',
            413: 'size 값으로 올바른 데이터을 넣지 않았음',
            414: '매개변수로 주지 않은 값이 있음'
        }
    )
    @jwt_required
    @api.expect(post_parser)
    def post(self, cloth_type):
        return method.post(cloth_type)

    @api.doc(
        description='등록한 제품을 취소하기 위한 API로, {type}에 Shirts, Shoes, Pants, Accessory 를 넣을 수 있다.',
        responses={
            200: '제품 등록 취소 성공',
            410: '{type} path에 Shirts, Shoes, Pants, Accessory 이외의 값을 줌',
            411: 'swagger docs에 나와있는 대로 params을 전달해 주세요.',
            412: '해당 url에 대해 제품이 존재하지 않거나 요청한 유저의 제품이 아님',
            413: '해당 url에 대한 제품은 이미 판매된 제품임'
        }
    )
    @jwt_required
    @api.expect(delete_parser)
    def delete(self, cloth_type):
        return method.delete(cloth_type)