# -*- coding: utf-8 -*-
"""
    flaskbb.auth.views
    ~~~~~~~~~~~~~~~~~~~~

    This view provides user authentication, registration and a view for
    resetting the password of a user if he has lost his password

    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint, request, redirect, flash, url_for
from flask import render_template
from jinja2 import TemplateNotFound
from flask import abort
from midstation.auth.forms import LoginForm, RegisterForm
from wechat_sdk import WechatBasic
from flask_login import (login_user, current_user, login_required, logout_user)
from midstation.user.views import user
from midstation.user.models import User

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/')
def wechat_token():
    if request.method == 'GET':
         return redirect(url_for('auth.login'))

    args = request.args
    token = 'midstation'
    echostr = args['echostr']

    signature = args['signature']
    timestamp = args['timestamp']
    nonce = args['nonce']


    # 实例化 wechat
    wechat = WechatBasic(token=token)
    # 对签名进行校验
    if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        return echostr

    return 'auth token fail'


@auth.route('/auth/register', methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            # if form.validate_username():
            user = form.save()
            login_user(user)
            flash("Thanks for registering. %s" % current_user.username, "success")
            return redirect(url_for('user.button_list'))
    try:
        return render_template('auth/register.html', title='Register', form=form)
    except TemplateNotFound:
        abort(404)


@auth.route("/auth/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user, authenticated = User.authenticate(form.username.data,
                                                form.password.data)

            if user and authenticated:
                login_user(user, remember=form.remember_me.data)
                flash('Logged successfully %s' % current_user.username, 'success')
                return redirect(url_for('user.button_list'))

            flash("Wrong Username or Password.", "danger")
            print 'Wrong Username'
            # return redirect('/auth/register')
    return render_template('auth/login.html',
        title='Sign In',
        form=form)

@auth.route('/auth/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))