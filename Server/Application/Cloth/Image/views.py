from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.Cloth.Image import method

cloth_namespace = api.namespace('Cloth', description='APIs for Request clothes')


@cloth_namespace.route('/Image/<string:type>/<int:number>')
class Image(Resource):
    @api.doc(
        description='HTML 코드에서 img 태그의 src 속성에 넣은 이미지 URL을 생성해주는 API (직접적으로 이 API에 접근할 필요가 없음)'
    )
    def get(self, type, number):
        return method.get(type, number)