# coding=utf-8
from flask import Blueprint, request

from models import User
from flask import session
from .procedure.process_procedure import Process
from utils.display_helper import DisplayHelper, Status

process = Blueprint('process', __name__)


@process.route('/instance', methods=['POST'])
def process_instance():
    """
    action == create 创建并启动流程
    """
    print request.cookies
    print session
    content = request.json
    if content.get('action') == 'create':
    #     process_name = content.get('process_name')
    #     form = content.get('form')
    #     code, msg, data = Process.create_process_instance(process_name, form)
    #     if code != Status.ok:
    #         return DisplayHelper.output(code, msg, data)
    #     process_instance_id = data.get('id')
    #     code, msg, data = Process.finish_curr_activity_start_next(process_instance_id)
    # return DisplayHelper.output(code, msg, data)
        acs = Process.get_curr_user_running_activities()
        return 'hello'

@process.route('/test')
def test():
    data = Process.create_process_instance('repair_apply', {"name": 'zhangsan'})
    print data
    # Process.init_process_define()
    return 'success'

