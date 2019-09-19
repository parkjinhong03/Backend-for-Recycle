from flask_restplus import Resource
from flask_jwt_extended import jwt_refresh_token_required
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.User.Login.Refresh import method


@api.route('/User/login/refresh',
           doc={'description': '만약 access_token의 만료일이 다 되었으면 refresh_token을 header에 넣어서 이 API를 호출해서,'
                               ' 새로운 access_token을 발급받을 수 있다.'})
class Refresh(Resource):
    @api.doc(responses={
        200: 'refresh_token 인증 성공 및 새 access_token 발급',
        401: 'refresg_token의 값이 header에 포함되지 않았음',
        422: 'refresh_token의 값이 외부 요인에 의해 변형됨',
    })
    @jwt_refresh_token_required
    def post(self):
        return method.post()