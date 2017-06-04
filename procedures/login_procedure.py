import json
import requests
from utils.WXBizDataCrypt import WXBizDataCrypt

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
    def get_login_session(cls, content):
        encryptedData = content['encryptedData']
        code = content['code']
        iv = content['iv']
        session_key, open_id = cls.get_open_id(code)
        wxbi = WXBizDataCrypt(appId=APPID, sessionKey=session_key)
        data = wxbi.decrypt(encryptedData, iv)
        data["session_key"] = session_key
        return 200, u'ok', None

    @classmethod
    def check_login_status(cls, cookies):
        pass

