# coding=utf-8
from bson import json_util
from flask import Blueprint, request

from models import User, ProcessDefine
from flask import session
from .procedure.process_procedure import Process
from utils.display_helper import DisplayHelper, Status

process = Blueprint('process', __name__)


@process.route('/instance', methods=['POST'])
def process_instance():
    """
    action == create 创建并启动流程
    action == finish
    """
    content = request.json
    if content.get('action') == 'create':
        process_name = content.get('process_name')
        form = content.get('form')
        code, msg, data = Process.create_process_instance(process_name, form)
        if code != Status.ok:
            return DisplayHelper.output(code, msg, data)
        process_instance_id = data.get('id')
        code, msg, data = Process.finish_curr_activity_start_next(process_instance_id)
    elif content.get('action') == 'finish':
        process_instance_id = content.get('process_id')
        code, msg, data = Process.finish_curr_activity_start_next(process_instance_id)
    elif content.get("action") == 'update_form':
        form = content.get('form')
        process_instance_id = content.get('process_id')
        code, msg, data = Process.update_form(process_instance_id, form)
    else:
        code, msg, data = Status.failed, u'action is not found', None
    return DisplayHelper.output(code, msg, data)



@process.route('/activities', methods=['GET'])
def get_activities():
    """
    view = get_wait 获取当前用户可领取任务
    :return:
    """
    view = request.args['view']
    if view == 'get_wait':
        code, msg, data = Process.get_wait_activities()
    if view == 'get_wait_order':
        code, msg, data = Process.get_wait_order()
    if view == 'get_wait_repair':
        code, msg, data = Process.get_wait_repair()
    if view == 'get_all_history':
        code, msg, data = Process.get_all_history()
    if view == 'get_end_history':
        code, msg, data = Process.get_end_history()
    if view == 'get_running':
        code, msg, data = Process.get_running_activities()
    if view == 'get_config':
        process_id = request.args['process_id']
        code, msg, data = Process.get_page_config(process_id)
    if view == 'get_process_data':
        process_id = request.args['process_id']
        code, msg, data = Process.get_process_data(process_id)
        data['process_data'] = DisplayHelper.mongoset_to_dict(data['process_data'])
        data['curr_data'] = DisplayHelper.mongoset_to_dict(data['curr_data'])
        for i in range(len(data['curr_participants'])):
            if isinstance(data['curr_participants'][i], User):
                data['curr_participants'][i] = DisplayHelper.mongoset_to_dict(data['curr_participants'][i])
        return json_util.dumps({
            "code": code,
            "msg": msg,
            "data": data
        })
    return DisplayHelper.output(code, msg, data, True)


@process.route('/init_process')
def process_define_init():
    Process.init_process_define()
    return 'success'


@process.route('/test')
def test():
    return 'test'
