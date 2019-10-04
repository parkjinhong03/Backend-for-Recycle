import pymysql


def connect():
    try:
        db = pymysql.connect(host="localhost", user="root", password="jinhong", db="recycle", charset="utf8")
    except:
        db = pymysql.connect(host="localhost", user="root", password="", db="recycle", charset="utf8")

    cursor = db.cursor()

    return db, cursor