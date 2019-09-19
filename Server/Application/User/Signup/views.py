from flask_restplus import Resource
import sys

sys.path.append('/Server')
from setting_api import real_api as api
from Application.User.Signup import method


@api.route('/User/signup')
class Signup(Resource):
    def get(self):
        return method.get()