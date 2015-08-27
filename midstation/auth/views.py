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


auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/')
def hello():
    try:
        return render_template("layout.html")
    except TemplateNotFound:
        abort(404)

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
        return redirect('/auth/register')
    return render_template('auth/login.html',
        title='Sign In',
        form=form)