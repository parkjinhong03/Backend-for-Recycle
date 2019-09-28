from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.User.Image import method

cloth_namespace = api.namespace('User', description='APIs for Request users')


@cloth_namespace.route('/Profile/<string:img_name>')
class Image(Resource):
    @api.doc(
        description='HTML 코드에서 img 태그의 src 속성에 넣을 프로필 이미지 URL을 생성해주는 API (직접적으로 이 API에 접근하면 이미지를 반환함)'
    )
    def get(self, img_name):
        return method.get(img_name)