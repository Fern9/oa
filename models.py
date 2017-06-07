# coding=utf-8
from oa import db
import datetime


class User(db.Document):
    wx_userinfo = db.DictField()  # 用户微信信息
    wx_open_id = db.StringField(required=True)
    name = db.StringField()  # 姓名
    phone = db.StringField()  # 联系电话
    address = db.StringField()  # 地址
    company = db.StringField()  # 工作单位
    age = db.IntField()  # 年龄
    email = db.EmailField()  # 邮箱
    register_time = db.DateTimeField(default=datetime.datetime.now)  # 注册时间
    edit_time = db.DateTimeField(default=datetime.datetime.now)  # 最后编辑时间
    role = db.ReferenceField('Role')


class Role(db.Document):
    name = db.StringField(unique=True, required=True)  # 角色名,唯一
    permission = db.ListField()  # 权限列表
    default = db.BooleanField()  # 是否为默认角色,默认角色为普通用户


class Permission():
    APPLY_REQUIRE = 1  # 申请维修
    EDIT_REPIRE_FORM = 2  # 编辑维修单
    MANAGE_USER = 3  # 用户管理
    AUTH_ROLE = 4  # 更改用户角色


def init_roles():
    for role in Role.objects.all():
        role.delete()
    common = Role(name="normal", permission=[Permission.APPLY_REQUIRE], default=True)
    repairer = Role(name="repair", permission=[Permission.APPLY_REQUIRE, Permission.EDIT_REPIRE_FORM],
                    default=False)
    admin = Role(name="admin", permission=[Permission.APPLY_REQUIRE, Permission.EDIT_REPIRE_FORM,
                                           Permission.AUTH_ROLE,
                                           Permission.MANAGE_USER], default=False)
    common.save()
    repairer.save()
    admin.save()
