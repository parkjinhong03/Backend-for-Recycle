from flask_restplus import reqparse


def parser(*args):
    return_list = []
    reqp = reqparse.RequestParser()

    for i in args:
        reqp.add_argument(i, type=str)

    request_args = reqp.parse_args()

    for i in args:
        return_list.append(request_args[i])

    return return_list