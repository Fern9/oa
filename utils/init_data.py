from process.procedure.process_procedure import Process
from utils.data_helper import DataHelper
from oa import app
from models import *


if __name__ == '__main__':
    try:
        app.app_context().push()
        ProcessDefine.objects().delete()
        ProcessInst.objects().delete()
        ActivityInst.objects().delete()
        Process.init_process_define()
        roles = Role.objects().all()
        if roles is None:
            DataHelper.init_roles()
        print 'init data success'
    except Exception as e:
        print e.message


