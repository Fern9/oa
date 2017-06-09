import json
import sys

import requests
from flask import session
from flask_login import login_user, logout_user

from models import User
from oa import login_manager
from utils.WXBizDataCrypt import WXBizDataCrypt
from utils.data_helper import Status

APPID = "wxe2bdfe83e46f876b"
SECRET = "6d5622b5ea562540da116daaec9e6db0"

wx_api_url = 'https://api.weixin.qq.com'

class LoginProcedure:
    @classmethod
    def get_open_id(cls, code):
        url = '/sns/jscode2session'
        data = {
            "appid": APPID,
            "secret": SECRET,
            "js_code": code,
            "grant_type": "authorization_code"
        }
        req = requests.get(wx_api_url + url, params=data)
        res = json.loads(req.text)
        return res.get('session_key'), res.get('openid')

    @classmethod
    def get_login_data(cls, content):
        encryptedData = content['encryptedData']
        code = content['code']
        iv = content['iv']
        session_key, open_id = cls.get_open_id(code)
        if session_key is None or open_id is None:
            return Status.failed, u'get session key and openid failed', None
        wxbi = WXBizDataCrypt(appId=APPID, sessionKey=session_key)
        data = wxbi.decrypt(encryptedData, iv)
        data["session_key"] = session_key
        data['open_id'] = open_id

        return Status.ok, u'ok', data


    @classmethod
    def check_login_status(cls, cookies):
        pass

    @classmethod
    def login(cls, content):
        """
        :param content: must include 'code'
        :return: login status
        """
        code, msg, data = cls.get_login_data(content)
        if code != Status.ok:
            return code, msg, None
        user = User.objects(wx_open_id=data['open_id']).first()
        if user is None:
            # UserProcedure.user_register(content)
            return Status.not_found, u'user not found', None
        # user = User.objects(wx_open_id=data['open_id']).first()
        login_user(user, remember=True, force=True)
        session['session_key'] = data['session_key']
        session['open_id'] = data['open_id']
        return Status.ok, u'ok', None

    @classmethod
    def logout(cls):
        logout_user()
        return Status.ok, u'ok', None


@login_manager.user_loader
def load_user(user_id):
    return User.objects(wx_open_id=user_id).first()
