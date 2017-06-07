# coding=utf-8
import json

class Status():
    ok = 200  # 成功
    failed = 400  # 失败
    unauth = 401  # 未授权
    not_found = 404  # 资源未找到
    forbidden = 403  # 没有权限


class DisplayHelper:
    @classmethod
    def output(cls, code=Status.ok, msg=u'', data=None):
        return json.dumps({
            "code": code,
            "msg": msg,
            "data": data
        })

