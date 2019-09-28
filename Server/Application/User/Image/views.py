from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.User.Image import method

cloth_namespace = api.namespace('User', description='APIs for Request users')

post_parser = api.parser()
post_parser.add_argument('JWT-Token', location='headers', required=True, help='회원 인증을 위해 User/login에서 받은 access_token을 Header에 포함해서 줘야함')
post_parser.add_argument('file', location='files', type='FileStorage', required=True, help='등록할 옷에 대한 사진(jpg, png만)')


@cloth_namespace.route('/Profile/<string:img_name>')
class Image(Resource):
    @api.doc(
        description='HTML 코드에서 img 태그의 src 속성에 넣을 프로필 이미지 URL을 생성해주는 API (직접적으로 이 API에 접근하면 이미지를 반환함)'
    )
    def get(self, img_name):
        return method.get(img_name)


@cloth_namespace.route('/Profile')
class Profile(Resource):
    @api.doc(
        description='해당 유저의 프로필 이미지 사진을 변경해주는 API로, JWT-token과 바꾼 이미지 사진을 줘야한다.',
        responses={
            200: '회원 프로필 사진 변경 완료'
        }
    )
    @api.expect(post_parser)
    @jwt_required
    def post(self):
        return method.post()