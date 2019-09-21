from flask import Flask
from flask_restplus import Api, Resource
from flask_jwt_extended import JWTManager


app = Flask(__name__)
api = Api(app, version='1.0', title='Re-cycle API', description='2019 공개 SW 개발자 대회 Backend API')

app.config['JWT_SECRET_KEY'] = 'super-secret'

jwt = JWTManager(app)

import setting_api
setting_api.setAPI(api)

from Application.User.Signup.views import Signup
from Application.User.Signup.Email.views import Email,EmailAuth
from Application.User.Login.views import Login
from Application.User.Login.Refresh.views import Refresh

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)