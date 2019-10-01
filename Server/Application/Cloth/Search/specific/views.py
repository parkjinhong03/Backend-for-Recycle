from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.Cloth.Search.specific import method

cloth_namespace = api.namespace('Cloth', description='APIs for Request clothes')


@cloth_namespace.route('/Specific/<string:type>/<string:image_name>')
class specific(Resource):
    @api.doc(
        description='{type}종류 옷중 이미지 파일 이름이 {image_name}인 옷의 세부 정보를 반환하는 API이다.',
        responses={
            200: '반환 성공',
            410: 'type에 [Shirts, Shoes, Pants, Accessory] 중 하나의 값을 주세요',
            411: '존재하지 않는 옷임'
        }
    )
    def get(self, type, image_name):
        return method.get(type, image_name)