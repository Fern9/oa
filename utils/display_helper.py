# coding=utf-8
import json
from bson import json_util
from flask_mongoengine import BaseQuerySet


class Status():
    ok = 200  # 成功
    failed = 400  # 失败
    unauth = 401  # 未授权
    not_found = 404  # 资源未找到
    forbidden = 403  # 没有权限


class DisplayHelper:
    @classmethod
    def mongoset_to_dict(cls, mongoset):
        return [ob.to_mongo().to_dict() for ob in mongoset]

    @classmethod
    def output(cls, code=Status.ok, msg=u'', data=None, is_mongo=False):
        if isinstance(data, BaseQuerySet) or is_mongo:
            data = cls.mongoset_to_dict(data)
            return json_util.dumps({
                "code": code,
                "msg": msg,
                "data": data
            })
        return json.dumps({
            "code": code,
            "msg": msg,
            "data": data
        })

    @classmethod
    def mongo_output(cls, code=Status.ok, msg=u'', data=None):
        return json_util.dumps({
            "code": code,
            "msg": msg,
            "data": data
        })
