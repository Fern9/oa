# coding=utf-8
from flask import session
from flask_login import current_user
from mongoengine import ValidationError

from models import User, Role
from utils.data_helper import DataHelper
from utils.display_helper import Status
from login_procedure import LoginProcedure


class UserProcedure:
    @classmethod
    def user_register(cls, content):
        """
        :param content:
        :return:  procedure 函数返回值都统一用三个参数：code,msg,data
        """
        user = User()
        code = content.get('code')
        session_key, openid = LoginProcedure.get_open_id(code)
        user.wx_open_id = openid
        content.pop('code')
        user.wx_userinfo = content.get('wx_userinfo')
        code, msg, data = DataHelper.init_object_from_dict(user, content.get('userinfo'))
        if code != Status.ok:
            return code, msg, data
        try:
            user = data
            if 'role' in content:
                role = Role.objects(name=content['role']).first()
                if role is None:
                    return Status.failed, u'can not find Role: ' + content['role'], None
            else:
                role = Role.objects(default=True).first()
            user.role = role
            user.save()
        except ValidationError as e:
            return Status.failed, e.message, None
        return Status.ok, u'ok', None

    @classmethod
    def get_curr_user_info(cls):
        if current_user is None:
            return Status.unauth, u'当前未登录', None
        return Status.ok, u'ok', current_user

    @classmethod
    def get_all_user_info(cls):
        users = User.objects.all()
        return Status.ok, u'ok', users

    @classmethod
    def get_user_info_by_openid(cls, openid):
        user = User.objects(wx_open_id=openid)
        if user is None:
            return Status.not_found, u'not found user', None
        return Status.ok, u'ok', user

    @classmethod
    def update_user(cls, user_id, content):
        user = User.objects.get(id=user_id)
        if 'wx_userinfo' in content:
            user.wx_userinfo = content.get('wx_userinfo')
        user = DataHelper.init_object_from_dict(user, content.get('userinfo'))
        user.save()

    @classmethod
    def update_curr_user(cls, content):
        if 'open_id' not in session:
            return Status.unauth, u'未找到登录信息', None
        open_id = session['open_id']
        user = User.objects(wx_open_id=open_id).first()
        cls.update_user(user.get_id(), content)
