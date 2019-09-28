from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.Cloth.Search import method

cloth_namespace = api.namespace('Cloth', description='APIs for Request clothes')

parser = api.parser()
parser.add_argument('input', location='path', required=True, help='Cloth/뒤의 경로에 원하는 검색 단어를 넣어서 호출하는 API로, 해당 단어에 대한 검색 결과를 반환해준다.')


@cloth_namespace.route('/Search/<string:input>')
class Input(Resource):
    @api.doc(
        description="원하는 단어를 입력하면 검색 결과를 반환해주는 API",
        responses={
            200: '데이터 반환 성공'
        }
    )
    @api.expect(parser)
    def get(self, input):
        return method.get(input)