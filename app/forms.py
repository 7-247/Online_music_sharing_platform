#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    # DataRequired，当你在当前表格没有输入而直接到下一个表格时会提示你输入
    username = StringField('用户名', validators=[DataRequired(message='请输入用户名')])
    password = PasswordField('密码', validators=[DataRequired(message='请输入密码')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='请输入用户名')])
    email = StringField('邮箱', validators=[DataRequired(
        message='请输入邮箱'), Email(message='不符合邮箱格式')])
    password = PasswordField('密码', validators=[DataRequired(message='请输入密码')])
    password2 = PasswordField(
        '重复密码', validators=[DataRequired(message='请再次输入密码'), EqualTo('password', message='请确认密码是否相同')])
    submit = SubmitField('注册')
    # 校验用户名是否重复

    def validate_username(self, username):
        try:
            user = User.get(User.name == username)  # 查
        except:
            return  # 没查到
        raise ValidationError('用户名重复了，请您重新换一个呗!')
    # 校验邮箱是否重复

    def validate_email(self, email):
        try:
            user = User.get(User.email == email)  # 查
        except:
            return  # 没查到
        raise ValidationError('邮箱重复了，请您重新换一个呗!')


class EditProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='请输入用户名!')])
    about_me = TextAreaField('关于我', validators=[Length(min=0, max=140)])
    submit = SubmitField('提交')
