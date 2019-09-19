from flask_restplus import reqparse
import RequestParser


def get():
    name, email, phone, password = RequestParser.parser('name', 'email', 'phone', 'password')

    print(name, email, phone, password)

    return 'Hello world!'