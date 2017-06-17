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
    define_name = db.StringField(unique=True)
    description = db.StringField()
    form_name = db.StringField()
    activities = db.SortedListField(db.EmbeddedDocumentField('ActivityDefine'), ordering='sequence')
    state = db.IntField()
    create_time = db.DateTimeField(default=datetime.datetime.now)
    update_time = db.DateTimeField()
    definer = db.StringField()


class ActivityDefine(db.EmbeddedDocument):
    define_name = db.StringField()
    description = db.StringField()
    sequence = db.IntField()
    participants = db.ListField(db.DictField())


class Participant(db.EmbeddedDocument):
    type = db.StringField()
    value = db.StringField()


class ProcessInst(db.Document):
    inst_name = db.StringField()
    process_define = db.ReferenceField('ProcessDefine')
    description = db.StringField()
    form = db.DictField()
    state = db.IntField()
    # activities = db.SortedListField(db.ReferenceField('ActivityInst'))
    creator = db.ReferenceField('User')
    start_time = db.DateTimeField(default=datetime.datetime.now)
    end_time = db.DateTimeField()


class ActivityInst(db.Document):
    inst_name = db.StringField()
    process_inst = db.ReferenceField('ProcessInst')
    activity_define = db.EmbeddedDocumentField('ActivityDefine')
    sequence = db.IntField()
    participants = db.ListField(db.DictField())
    state = db.IntField()
    start_time = db.DateTimeField()
    end_time = db.DateTimeField()


class DefineStatus(object):
    active = 1
    inactive = -1
    old_version = 0


class InstanceStatus(object):
    new = 1 #新建
    wait = 2 #等待领取
    running = 3 #正在运行
    block = 4  #挂起
    dead = 5  #结束
