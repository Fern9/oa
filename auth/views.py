# coding=utf-8
from flask import request
from procedures.user_procedure import UserProcedure
from procedures.login_procedure import LoginProcedure
from utils.display_helper import Status, DisplayHelper
from . import auth
from utils.data_helper import DataHelper

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
        content.pop('action')
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
    view == get_all: 获取所有用户信息
    :return:
    """
    params = request.args
    view = params['view']
    if view == "get_curr_user_info":
        code, msg, data = UserProcedure.get_curr_user_info()
        data = DataHelper.mongoset_to_dict(data)
    elif view == "get_all":
        code, msg, data = UserProcedure.get_all_user_info()
        data = DataHelper.mongoset_to_dict(data)
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


