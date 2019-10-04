from flask_jwt_extended import get_jwt_identity
from db_connect import connect


def get():
    db, cursor = connect()
    return_dict = {}

    _user = get_jwt_identity()
    return_dict['name'] = _user

    sql = f'SELECT * FROM UserImage WHERE name = "{_user}"'
    cursor.execute(sql)
    ImageUrl = cursor.fetchone()[1]

    return_dict['ImageUrl'] = ImageUrl

    sql = f'SELECT * FROM UserRank WHERE name = "{_user}"'
    try:
        cursor.execute(sql)
        return_dict['rank'] = cursor.fetchone()[1]
    except:
        pass

    sql = f'SELECT * FROM userlog WHERE name = "{_user}"'
    cursor.execute(sql)
    user_data = cursor.fetchone()
    email = str(user_data[1])
    phone = str(user_data[2])

    email_front = email.split('@')[0]
    email_back = email.split('@')[1]

    email_front = email_front[0:len(email_front) // 2- 1]

    for i in range(len(email_front) // 2 - 1, len(email_front)):
        email_front = email_front + '*'

    return_dict['email'] = email_front + "@" + email_back

    phone_first = phone[0:3]
    phone_last = phone[7:11]

    phone = phone_first + "-****-" + phone_last
    return_dict['phone'] = phone

    db.close()
    return return_dict