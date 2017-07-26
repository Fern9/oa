from models import Role
from process.procedure.process_procedure import Process
from utils.data_helper import DataHelper
from oa import app


if __name__ == '__main__':
    try:
        app.app_context().push()
        Process.init_process_define()
        roles = Role.objects().all()
        if roles is None:
            DataHelper.init_roles()
        print 'init data success'
    except Exception as e:
        print e.message


