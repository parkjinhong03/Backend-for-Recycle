from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.Cloth.Search.random import method

cloth_namespace = api.namespace('Cloth', description='APIs for Request clothes')


@cloth_namespace.route('/random')
class Random(Resource):
    @api.doc(
        description='등록된 옷들 중 랜덤으로 6개를 뽑아 옷에 대한 정보를 반환해주는 API',
        responses={
            200: '랜덤 데이터 반환 성공'
        }
    )
    def get(self):
        return method.get()