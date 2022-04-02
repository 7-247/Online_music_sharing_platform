#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from datetime import datetime
from re import VERBOSE
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from flask_login import UserMixin  # 不知道有没有用
from app import BaseModel
import peewee as pw


class User(UserMixin,
           BaseModel):  # 标准格式 继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    #id = pw.IntegerField(primary_key=True)  # 主键
    username = pw.CharField(max_length=64, index=True, unique=True)  # 唯一的用户名
    email = pw.CharField(max_length=120, index=True, unique=True)  # 唯一的邮箱
    about_me = pw.CharField(max_length=256)
    last_seen = pw.DateField(default=datetime.utcnow())
    password_hash = pw.CharField(max_length=128)

    def set_password(self, password):
        self.password_hash = str(generate_password_hash(password))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<用户名:{}>'.format(self.username)

    def avatar(self, size):  # 根据邮箱自动获取分形图的API
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://gravatar.zeruns.tech/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class Music(BaseModel):  # 标准格式 继承自BaseModel，直接关联db，并且也继承了Model Model有提供增删查改的函数
    #id = pw.IntegerField(primary_key=True)
    music_name = pw.CharField(verbose_name='音乐名',
                              max_length=128,
                              null=False,
                              index=True)
    singer_name = pw.CharField(verbose_name='歌手名',
                               max_length=128,
                               null=False,
                               default='key')
    music_type = pw.CharField(verbose_name='歌曲类型',
                              max_length=16,
                              null=False,
                              default='mp3')
    album_name = pw.CharField(verbose_name='专辑名',
                              max_length=128,
                              null=False,
                              default='NO FOUND')

    def __repr__(self):
        return '<Music {}>'.format(self.music_name + ' - ' + self.singer_name)


class SongSheet(BaseModel):
    #id = pw.IntegerField(primary_key=True)
    userid = pw.IntegerField(index=True)  # 唯一的用户名,对应
    sheet_name = pw.CharField(verbose_name='歌单名',
                              max_length=32,
                              null=False,
                              index=True)
    musiclist = pw.CharField(verbose_name='歌曲列表', max_length=1024, default='')

    #由于没有列表，只好用字符串了,歌曲id之间以'-'分割
    def __repr__(self):
        return '<SongSheet {}{}>'.format(self.user_id, self.sheet_name)
