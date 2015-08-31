# -*- coding: utf-8 -*-
__author__ = 'qitian'

from flask import Blueprint, request, render_template, abort, redirect, url_for
from jinja2 import TemplateNotFound
from midstation.user.models import User
from midstation.user.models import Button
user = Blueprint('user', __name__, template_folder='templates')


@user.route('/button_list')
def button_list():
    try:
        #get buttons
        buttons = get_buttons(1)
        print buttons
        return render_template("user/button_list.html", buttons=buttons)
    except TemplateNotFound:
        abort(404)

@user.route('/button/<node_id>')
def button_profile(node_id):
    button = Button.query.filter_by(node_id=node_id).first()
    if not button:
        redirect(url_for('button_list'))
    try:
        return render_template('user/button_profile.html', button=button)
    except TemplateNotFound:
        abort(404)

def get_buttons(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return user.all_buttons(page=1)