# coding=utf-8
import json
from flask import request
from procedures.user_procedure import UserProcedure
from procedures.login_procedure import LoginProcedure
from utils.display_helper import Status, DisplayHelper
from . import auth


@auth.route('/user', methods=['POST'])
def user():
    """
    action == register:注册
    action == login:登录
    ...
    """
    content = request.json
    action = content['action']
    if action == "register":
        code, msg, data = UserProcedure.user_register(content)
    else:
        code = Status.failed
        msg = u'无此 action'
        data = None
    return DisplayHelper.output(code, msg, data)


@auth.route('/user', methods=['GET'])
def user_get():
    """
    view == get_curr_user_info:获取用户信息
    view ==  xxx:获取用户 xxx
    :return:
    """
    params = request.args
    view = params['view']
    if view == "get_curr_user_info":
        code, msg, data = UserProcedure.get_user_info()
    else:
        code = Status.failed
        msg = u'无此 action'
        data = None
    return DisplayHelper.output(code, msg, data)


@auth.route('/login', methods=['POST'])
def wx_login():
    content = request.json
    code, msg, data = LoginProcedure.login(content)
    return DisplayHelper.output(code, msg, data)


@auth.route('/test')
def test():
    return 'hello world'


