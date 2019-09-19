from flask import Flask
from flask_restplus import Api, Resource
from flask_jwt_extended import JWTManager


app = Flask(__name__)
api = Api(app)

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'

jwt = JWTManager(app)

import setting_api
setting_api.setAPI(api)

from Application.User.Signup.views import Signup
from Application.User.Signup.Email.views import Email,EmailAuth

if __name__ == '__main__':
    app.run(host="10.156.147.138", port=5000, debug=True)