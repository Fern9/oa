# coding=utf-8
from flask.ext.login import UserMixin
from flask_mongoengine import MongoEngine

import datetime

db = MongoEngine()


class User(db.Document, UserMixin):
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

    def get_id(self):
        return self.wx_open_id


class Role(db.Document):
    name = db.StringField(unique=True, required=True)  # 角色名,唯一
    permission = db.ListField()  # 权限列表
    default = db.BooleanField()  # 是否为默认角色,默认角色为普通用户


class Permission():
    APPLY_REQUIRE = 1  # 申请维修
    EDIT_REPIRE_FORM = 2  # 编辑维修单
    MANAGE_USER = 3  # 用户管理
    AUTH_ROLE = 4  # 更改用户角色


class RepairForm(db.Document):
    apply_user = db.ReferenceField("User")
    trouble_thing = db.StringField()
    description = db.StringField()
    address = db.StringField()
    phone = db.StringField()
    comment = db.StringField()


class ProcessDefine(db.Document):
    define_name = db.StringField()
    description = db.StringField()
    form_name = db.StringField()
    activities = db.SortedListField(db.EmbeddedDocumentField('ActivityDefine'), odering='sequence', reverse=True)
    state = db.IntField()
    create_time = db.DateTimeField()
    update_time = db.DateTimeField()
    definer = db.StringField()


class ActivityDefine(db.EmbeddedDocument):
    define_name = db.StringField()
    description = db.StringField()
    sequence = db.IntField()
    participant = db.ListField()


class Participant(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value


class ProcessInst(db.Document):
    inst_name = db.StringField()
    process_define = db.ReferenceField('ProcessDefine')
    description = db.StringField()
    form = db.DictField()
    state = db.IntField()
    activities = db.SortedListField(db.EmbeddedDocumentField('ActivityInst'), odering='sequence', reverse=True)
    creator = db.ReferenceField('User')
    start_time = db.DateTimeField()
    end_time = db.DateTimeField()


class ActivityInst(db.EmbeddedDocument):
    inst_name = db.StringField()
    activity_define = db.ReferenceField('ActivityDefine')
    sequence = db.IntField()
    participants = db.ListField()
    state = db.IntField()
    start_time = db.DateTimeField()
    end_time = db.DateTimeField()
