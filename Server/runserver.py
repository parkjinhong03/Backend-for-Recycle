from flask import Flask
from flask_restplus import Api, Resource
from flask_jwt_extended import JWTManager
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='Re-cycle API', description='2019 공개 SW 개발자 대회 Backend API')

app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWTManager(app)

import setting_api
setting_api.setAPI(api)

from Application.User.Signup.views import Signup
from Application.User.Signup.Email.views import Email,EmailAuth
from Application.User.Login.views import Login
from Application.User.Login.Refresh.views import Refresh
from Application.Cloth.Search.random.views import Random
from Application.Cloth.Image.views import Image
from Application.Cloth.Registration.views import Register
from Application.Cloth.Search.Separation.views import Separation
from Application.Cloth.Search.Latest.views import Latest
from Application.Cloth.Search.views import Input
from Application.Cloth.Search.User.views import MyCloth
from Application.Cloth.Reservation.views import Reservation
from Application.Cloth.Basket.views import Basket
from Application.User.Image.views import Image
from Application.User.My.views import My
from Application.User.Rank.views import Rank
from Application.Cloth.Borrow.views import Borrow
from Application.Cloth.Buy.views import Buy
from Application.User.Payment.views import Payment
from Application.Cloth.Search.specific.views import specific

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)