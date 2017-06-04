# coding=utf-8
import json
from enum import Enum


class Status:
    ok = 7200  # 成功
    failed = 7400  # 失败
    not_found = 7404  # 资源未找到
    forbidden = 7403  # 没有权限


class DisplayHelper:
    @classmethod
    def output(cls, code=Status.ok, msg=u'', data=None):
        return json.dumps({
            "code": code,
            "msg": msg,
            "data": data
        })
