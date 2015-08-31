# -*- coding: utf-8 -*-
"""
    flaskbb.auth.views
    ~~~~~~~~~~~~~~~~~~~~

    This view provides user authentication, registration and a view for
    resetting the password of a user if he has lost his password

    :copyright: (c) 2014 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint, request, redirect, flash
from flask import render_template
from jinja2 import TemplateNotFound
from flask import abort
from midstation.auth.forms import LoginForm
from wechat_sdk import WechatBasic

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/')
def wechat_token():

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


@auth.route('/auth/register')
def register():
    try:
        return render_template('auth/register.html')
    except TemplateNotFound:
        abort(404)

# @auth.route("/auth/login", methods=["GET", "POST"])
# def login():
#     """
#     Logs the user in
#     """
#     form = LoginForm(request.form)
#     if form.validate_on_submit():
#         print form.username.data
#     print hello
#     return render_template("auth/login.html", form=form)


@auth.route("/auth/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.username.data + '", remember_me=' +str(form.remember_me.data))
        name = form.username.data
        password = form.password.data
        return redirect('/station/button_list.html')
        # return redirect('/auth/register')
    return render_template('auth/login.html',
        title='Sign In',
        form=form)