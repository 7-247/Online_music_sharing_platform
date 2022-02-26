#from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask
import peewee as pw

app = Flask(__name__)
app.config["SECRET_KEY"] = 'b8a0e5e48f7e4577a020b8502dcb7fc8'
login = LoginManager(app)
# py_peewee���ӵ����ݿ���
db = pw.MySQLDatabase('flask_web',
                      host='127.0.0.1',
                      user='root',
                      passwd='tongjigzy_02',
                      charset='utf8',
                      port=3306)


class BaseModel(pw.Model):
    class Meta:
        database = db  # ��ʵ�������ݿ���а�


from app import models  ##��һ�б�������������Ƶ�����ȥ
# �������ݿ�
db.connect()

# �������ݱ�

models.User.create_table()

models.SongSheet.create_table()
from app import music, songsheet
from app import routes, find, playerlist, songsheet
