import json
import requests
from utils.WXBizDataCrypt import WXBizDataCrypt
from flask_login import login_user, logout_user
from oa import login_manager
from auth.models import User
from flask import session
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
        print(req.text)
        res = json.loads(req.text)
        return res['session_key'], res['openid']

    @classmethod
    def get_login_data(cls, content):
        encryptedData = content['encryptedData']
        code = content['code']
        iv = content['iv']
        session_key, open_id = cls.get_open_id(code)
        wxbi = WXBizDataCrypt(appId=APPID, sessionKey=session_key)
        data = wxbi.decrypt(encryptedData, iv)
        data["session_key"] = session_key
        data['open_id'] = open_id
        return Status.ok.value, u'ok', data

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
        if code != Status.ok.value:
            return code, msg, None
        user = User.objects(wx_open_id=data['open_id']).first()
        if user is None:
            return Status.not_found.value, u'user not found', None
        login_user(user, remember=True)
        session['session_key'] = data['session_key']
        session['open_id'] = data['open_id']
        return Status.ok.value, u'ok', None






@login_manager.user_loader
def load_user(user_id):
    return User.objects(_id=user_id).first()
