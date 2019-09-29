from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.User.My import method

cloth_namespace = api.namespace('User', description='APIs for Request users')


@cloth_namespace.route('/My')
class My(Resource):
    @api.doc(
        description="해당 유저의 프로필 사진 URL, 이름, 등급을 반환해주는 API로, JWT-token을 포함해서 줘야한다.",
        responses={
            200: '데이터 반환 성공'
        }
    )
    @jwt_required
    def get(self):
        return method.get()