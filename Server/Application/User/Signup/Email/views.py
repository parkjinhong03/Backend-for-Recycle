from flask_restplus import Resource
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.User.Signup.Email import method


@api.route('/User/signup/email')
class Email(Resource):
    def post(self):
        return method.post1()


@api.route('/User/signup/email/auth')
class EmailAuth(Resource):
    def post(self):
        return method.post2()