from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.Cloth.Search.Separation import method

cloth_namespace = api.namespace('Cloth', description='APIs for Request clothes')

get_parser = api.parser()
get_parser.add_argument('cloth_type', location='path', required=True, help='Cloth/ 뒤의 경로에 넣는 값으로, Shirts, Shoes, Pants, Accessory 를 넣을 수 있다.')

search_response = api.model('search_type_response', {
    'name': fields.String,
    'image_url': fields.String,
    'title': fields.String,
    'description': fields.String,
    'price': fields.Integer,
    'size': fields.String,
    'first_date': fields.String
})


@cloth_namespace.route('/Type/<string:cloth_type>')
class Separation(Resource):
    @api.response(200, '해당 카테고리의 모든 옷 정보 반환 성공', search_response)
    @api.doc(
        descripttion='원하는 카테고리의 옷에 대한 정보를 랜덤으로 반환해주는 API',
        responses={
            410: '{cloth_type} path에 Shirts, Shoes, Pants, Accessory 이외의 값을 줌'
        }
    )
    @api.expect(get_parser)
    def get(self, cloth_type):
        return method.get(cloth_type)