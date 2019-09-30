from flask_restplus import Resource, fields
from flask_jwt_extended import jwt_required
import sys
from PIL import Image
import base64
from io import BytesIO

sys.path.append('/Server')
from setting_api import real_api as api
import RequestParser


@api.route('/test')
class test(Resource):
    def get(self):
        img_data = str(RequestParser.parser('binary')[0])

        print(img_data)
        print(base64.b64decode(img_data))

        with open('Data/text1.png', 'wb') as f:
            f.write(base64.b64decode(img_data))
