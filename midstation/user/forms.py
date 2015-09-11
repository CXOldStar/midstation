# -*- coding: utf-8 -*-
__author__ = 'qitian'
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from midstation.user.models import User
from flask_login import current_user

class UserInfoForm(Form):
    username = StringField(u'用户名', validators=[DataRequired()])
    telephone = StringField(u'电话')
    mobile_phone = StringField(u'手机')
    address = StringField(u'地址')

    def save_form(self):
        current_user.username = self.username.data
        current_user.telephone = self.telephone.data
        current_user.mobile_phone = self.mobile_phone.data
        current_user.address = self.address.data

        current_user.save()

