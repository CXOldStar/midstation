# -*- coding: utf-8 -*-
__author__ = 'qitian'

from flask import Blueprint, request, render_template, abort, redirect, url_for
from jinja2 import TemplateNotFound
from midstation.user.models import User
from midstation.user.models import Button

wechat = Blueprint('wechat', __name__, template_folder='templates')


@wechat.route('/')
def wchat():
    try:
        #get buttons
        print 'wechat token'
        return 'Hello'
    except TemplateNotFound:
        abort(404)