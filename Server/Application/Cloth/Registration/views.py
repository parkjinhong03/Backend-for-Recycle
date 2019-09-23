from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.Cloth.Registration import method

cloth_namespace = api.namespace('Cloth', description='APIs for Request clothes')

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type='FileStorage', required=True)
upload_parser.add_argument('description', type=str, required=True)
upload_parser.add_argument('price', type=int,  required=True)
upload_parser.add_argument('size', type=int, required=True)


@cloth_namespace.route('/Register/<string:cloth_type>')
class Register(Resource):
    @api.doc(
        description='중고로 거래할 제품을 등록해주는 API로, {type}에 Shirts, Shoes, Pants, Accessory 를 넣을 수 있다.',
        responses={
            200: '제품 등록 성공',
            410: '{type} path에 Shirts, Shoes, Pants, Accessory 이외의 값을 줌',
            411: '전달한 파일의 확장자가 jpg, png 외의 파일임'
        }
    )
    @api.expect(upload_parser)
    def post(self, cloth_type):
        return method.post(cloth_type)