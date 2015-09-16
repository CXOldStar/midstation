# -*- coding: utf-8 -*-

from datetime import datetime

from flask_wtf import Form, RecaptchaField
from wtforms import (StringField, SelectField, SubmitField)
from wtforms.validators import DataRequired
from midstation.user.models import User, Service, Customer
from flask_login import current_user


class ButtonForm(Form):
    node_id = StringField(u'node_id', validators=[DataRequired()])
    service = SelectField(u'服务', validators=[DataRequired()])
    customer = SelectField(u'客户')

    submit = SubmitField(u'保存')

    def __init__(self, *args, **kwargs):
        self.service.choices = [(obj.id, obj.name) for obj in Service.query.filter_by(user_id=current_user.id).all()]
        self.customer.choices = [(obj.id, obj.name) for obj in Customer.query.filter_by(user_id=current_user.id).all()]


    def auth(self):
        users = User.query.filter_by(username=self.username.data).all()
        for user in users:
            if user.id == self.password.data:
                return True

        return False
