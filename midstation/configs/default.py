# -*- coding: utf-8 -*-
"""
    midstation.configs.default
    ~~~~~~~~~~~~~~~~~~~~~~~

    This is the default configuration for FlaskBB that every site should have.
    You can override these configuration variables in another class.


"""
import os


class DefaultConfig(object):

    # Get the app root path
    #            <_basedir>
    # ../../ -->  flaskbb/flaskbb/configs/base.py
    _basedir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(
                            os.path.dirname(__file__)))))

    DEBUG = True
    TESTING = False

    # Logs
    # If SEND_LOGS is set to True, the admins (see the mail configuration) will
    # recieve the error logs per email.
    SEND_LOGS = False

    # The filename for the info and error logs. The logfiles are stored at
    # flaskbb/logs
    INFO_LOG = "info.log"
    ERROR_LOG = "error.log"

    # Default Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + _basedir + '/' + \
                              'test.sqlite'

    # This will print all SQL statements
    SQLALCHEMY_ECHO = True

    # Security
    # This is the secret key that is used for session signing.
    # You can generate a secure key with os.urandom(24)
    SECRET_KEY = 'secret key'

    # Protection against form post fraud
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = "reallyhardtoguess"

    # Searching
    WHOOSH_BASE = os.path.join(_basedir, "whoosh_index")

    # Auth
    LOGIN_VIEW = "auth.login"
    REAUTH_VIEW = "auth.reauth"
    LOGIN_MESSAGE_CATEGORY = "error"

    # Caching
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 60

    ## Captcha
    RECAPTCHA_ENABLED = False
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = "your_public_recaptcha_key"
    RECAPTCHA_PRIVATE_KEY = "your_private_recaptcha_key"
    RECAPTCHA_OPTIONS = {"theme": "white"}

    ## Mail
    MAIL_SERVER = "localhost"
    MAIL_PORT = 25
    MAIL_USE_SSL = False
    MAIL_USE_TLS = False
    MAIL_USERNAME = "noreply@example.org"
    MAIL_PASSWORD = ""
    MAIL_DEFAULT_SENDER = ("Default Sender", "noreply@example.org")
    # Where to logger should send the emails to
    ADMINS = ["admin@example.org"]

    # Flask-Redis
    REDIS_ENABLED = False
    REDIS_URL = "redis://:123456@183.230.40.230:6379"
    REDIS_DATABASE = 0

    # URL Prefixes
    STATION_URL_PREFIX = "/station"
    USER_URL_PREFIX = "/user"
    AUTH_URL_PREFIX = "/auth"
    ADMIN_URL_PREFIX = "/admin"
    WECHAT_URL_PREFIX = "/wechat"
    SERVICE_URL_PREFIX = '/service'
    CUSTOMER_URL_PREFIX = '/customer'
    ORDER_URL_PREFIX = '/order'

    # Smart Button
    GATEWAY_ID = 'a2d790e1-1670-1217-0000-000db93db700'
    ORGANIZATION = 'niot'
    LINKLAB_USERNAME = 'niot.user'
    LINKLAB_PASSWORD = 'Ni0t!0715'

    # Wechat
    WECHAT_TOKEN = 'midstation'
    WECHAT_APPID = 'wx6b84ff9cb6f9a54e'
    WECHAT_APPSECRET = '4e09e5b35198bdbf35b90a65d5f76af4'
    AUTH_KEY_EXPIRE = 300           # 微信验证码过去时间（min）
    # Auth
    LOGIN_VIEW = "auth.login"

    # Protection against form post fraud
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = "reallyhardtoguess"


