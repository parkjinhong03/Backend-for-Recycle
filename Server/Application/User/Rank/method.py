from db_connect import cursor, db
from flask_jwt_extended import get_jwt_identity
import RequestParser


def put():
    _user = get_jwt_identity()

    rank = RequestParser.parser('rank')[0]
    print(rank)

    if rank is None:
        return {"message": "docs에서 나온데로 params를 달라!", "code": 410}

    rank_list = ['Normal', 'VIP', 'VVIP']

    if rank not in rank_list:
        return {"message": "rank의 VALUE 값으로 [Normal, VIP, VVIP]만을 주세요", "code": 411}, 411

    sql = f'SELECT * FROM UserRank WHERE name = "{_user}"'
    cursor.execute(sql)

    rank_data = cursor.fetchone()

    if rank_data[1] == rank:
        return {"message": "이미 현재 등급인 상태 입니다.", "code": 412}, 412

    sql = f'UPDATE UserRank SET rank = "{rank}" WHERE name = "{_user}"'
    cursor.execute(sql)
    db.commit()

    return {"message": "해당 회원 등급 바꾸기 성공", "code": 200}, 200