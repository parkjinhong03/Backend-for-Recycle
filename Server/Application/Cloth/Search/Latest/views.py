from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.Cloth.Search.Latest import method

cloth_namespace = api.namespace('Cloth', description='APIs for Request clothes')


@cloth_namespace.route('/Latest')
class Latest(Resource):
    @api.doc(
        description='가장 최신에 등록된 옷을 차례대로 10개씩 반환해 주는 API',
        responses={
            200: '데이터 반환 성공'
        }
    )
    def get(self):
        return method.get()