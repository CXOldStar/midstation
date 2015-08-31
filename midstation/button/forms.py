# -*- coding: utf-8 -*-

from datetime import datetime

from flask_wtf import Form, RecaptchaField
from wtforms import (StringField, PasswordField, BooleanField, HiddenField,
                     SubmitField)
from wtforms.validators import (DataRequired, InputRequired, Email, EqualTo,
                                regexp, ValidationError, Length)
from midstation.user.models import User


class ButtonForm(Form):
    username = StringField(u'用户名', [Length(min=4, max=25)])
    password = PasswordField(u'密码', [Length(min=6, max=25)])
    remember_me = BooleanField(u'记住我', default=False)

    submit = SubmitField(u'登陆')

    def auth(self):
        users = User.query.filter_by(username=self.username.data).all()
        for user in users:
            if user.id == self.password.data:
                return True

        return False


# class LoginForm(Form):
#     username = StringField('username', validators=[InputRequired()])
#     password = PasswordField('password', validators=[Length(min=6, max=20)])
#     remember_me = BooleanField(u'记住我', default=False)
#     submit = SubmitField(u'登陆')