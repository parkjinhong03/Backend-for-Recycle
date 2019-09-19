import pymysql

db = pymysql.connect(host="localhost", user="root", password="jinhong", db="recycle", charset="utf8")
cursor = db.cursor()