from flask import Blueprint, request
from .procedure.process_procedure import Process
from utils.display_helper import DisplayHelper

process = Blueprint('process', __name__)

@process.route('/instance')
"""
action == create 创建并启动流程
"""
def process():
    content = request.json()
    if content.get('action') == 'create':
        process_name = content.get('process_name')
        form = content.get('form')
        code, msg, data = Process.create_process_instance(process_name, form)
    return DisplayHelper.output(code, msg, data)

@process.route('/test')
def test():
    data = Process.create_process_instance('repair_apply', {"name":'zhangsan'})
    print data
    # Process.init_process_define()
    return 'success'
