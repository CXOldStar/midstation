# -*- coding: utf-8 -*-
__author__ = 'qitian'

from flask import Blueprint, request, render_template, abort, redirect, url_for, flash
from jinja2 import TemplateNotFound
from midstation.user.models import User
from midstation.user.models import Button
from flask_login import login_required, current_user
from midstation.user.forms import UserInfoForm

user = Blueprint('user', __name__, template_folder='templates')


@user.route('/button_list')
@login_required
def button_list():
    try:
        #get buttons
        buttons = get_buttons(1)
        print buttons
        return render_template("user/button_list.html", buttons=buttons)
    except TemplateNotFound:
        abort(404)

@user.route('/button/<node_id>')
@login_required
def button_profile(node_id):
    if node_id == 0:
        button = Button()
    else:
        button = Button.query.filter_by(node_id=node_id).first()

    if not button:
        redirect(url_for('user.button_list'))
    try:
        return render_template('user/button_profile.html', button=button)
    except TemplateNotFound:
        abort(404)

@user.route('/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    form = UserInfoForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.save_form()
            flash(u'保存成功', category='success')
    # return render_template('user/test_jquery.html', user=current_user, form=form)
    return render_template('user/user_profile.html', user=current_user, form=form)




def get_buttons(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return user.all_buttons(page=1)

