from flask_jwt_extended import get_jwt_identity, create_access_token


def post():
    current_id = get_jwt_identity()
    access_token = create_access_token(identity=current_id)

    return {"message": "access_token 재발급 완료", "access_token": access_token}