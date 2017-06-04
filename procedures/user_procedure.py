# coding=utf-8
from mongoengine import ValidationError

from auth.models import User, Role
from utils.data_helper import DataHelper
from utils.display_helper import Status


class UserProcedure:
    @classmethod
    def user_register(cls, content):
        """
        :param content:
        :return:  procedure 函数返回值都统一用三个参数：code,msg,data
        """
        user = User()
        code, msg, data = DataHelper.init_object_from_dict(user, content)
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
