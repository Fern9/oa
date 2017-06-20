# coding:utf-8
import json
import os

from flask import session

import settings
from flask_login import current_user
from models import ProcessDefine, ActivityDefine, ProcessInst, User, ActivityInst, InstanceStatus, Participant
from utils.display_helper import Status


class Process():
    def __init__(self):
        pass

    @classmethod
    def init_process_define(cls):
        json_file_path = os.path.join(settings.APP_PATH, 'process/repair_apply_process_define.json')
        with open(json_file_path) as json_file:
            define = json.load(json_file)
        for obj in ProcessDefine.objects():
            obj.delete()
        process_define = ProcessDefine()
        for key in define:
            if key != 'activities':
                setattr(process_define, key, define.get(key))
        activities = define.get('activities')
        for activity in activities:
            activity_define = ActivityDefine()
            for key in activity:
                if key != 'participant':
                    setattr(activity_define, key, activity.get(key))
                else:
                    for participant in activity.get('participants'):
                        # par = Participant(type=participant['type'], value=participant['value'])
                        activity_define.participants.insert(p_object=participant)
            process_define.activities.append(activity_define)
        process_define.save()

    @classmethod
    def create_process_instance(cls, define_name, form):
        process_define = ProcessDefine.objects(define_name=define_name).first()
        if process_define is None:
            return Status.not_found, u'not find process define', None
        process_instance = ProcessInst()
        process_instance.inst_name = process_define.define_name
        process_instance.process_define = process_define
        process_instance.description = process_define.description
        process_instance.state = 1
        process_instance.form = form
        if 'open_id' not in session:
            return Status.unauth, u'need to login', None
        curr_user = User.objects(wx_open_id=session['open_id']).first()
        process_instance.creator = curr_user
        process_instance.save()
        is_start = True
        for activity in process_define.activities:
            activity_inst = ActivityInst()
            activity_inst.inst_name = activity.define_name
            activity_inst.process_inst = process_instance
            activity_inst.activity_define = activity
            activity_inst.state = InstanceStatus.new
            activity_inst.sequence = activity.sequence
            activity_inst.participants = []
            if is_start:
                activity_inst.state = InstanceStatus.running
                participant = Participant(type='user', value=str(current_user.id))
                activity_inst.participants.append(participant)
                activity_inst.form = form
                is_start = False
            activity_inst.save()
        return Status.ok, u'ok', {'id': process_instance.id}

    @classmethod
    def finish_curr_activity_start_next(cls, process_inst_id):
        process_instance = ProcessInst.objects().get(id=process_inst_id)
        # 如果流程不处于运行状态，直接返回失败
        if process_instance.state == InstanceStatus.dead:
            return Status.failed, u'流程处于非运行状态', None
        activities = ActivityInst.objects(process_inst=process_instance).all()
        for activity in activities:
            if activity.state == InstanceStatus.running:
                curr_activity = activity
                break
        next_activity = ActivityInst.objects(process_inst=process_instance, sequence=curr_activity.sequence + 1).first()
        curr_activity.state = InstanceStatus.dead
        curr_activity.save()
        # 如果当前为最后一环互动，则直接结束流程
        if next_activity is None:
            process_instance.state = InstanceStatus.dead
            process_instance.save()
        else:
            next_activity.state = InstanceStatus.wait
            next_activity.save()
        return Status.ok, u'ok', None

    @classmethod
    def run_activity(cls, activity_id, user):
        activity = ActivityInst.objects().get(id=activity_id)
        if activity.state != InstanceStatus.wait:
            return Status.failed, u'该活动不处于待领取状态，不能领取', None
        activity.state = InstanceStatus.running
        participant = Participant(type='user', value=user.id)
        activity.participants.append(participant)
        activity.save()
        return Status.ok, u'ok', None

    @classmethod
    def get_wait_activities(cls, user):
        participant_dict1 = {'type': 'user', 'vaule': user.id}
        participant_dict2 = {'type': 'role', 'vaule': user.role.name}
        activities1 = set(
            ActivityInst.objects(participants__contains=participant_dict1, state=InstanceStatus.wait).all())
        activities2 = set(
            ActivityInst.objects(participants__contains=participant_dict2, state=InstanceStatus.wait).all())
        activities = [x for x in (activities1 | activities2)]
        return activities

    @classmethod
    def get_running_activities(cls, user):
        activities = ActivityInst.objects(participants__match={"type": "user", "value": str(user.id)}, state=InstanceStatus.running).all()
        return activities

    @classmethod
    def get_curr_user_running_activities(cls):
        return cls.get_running_activities(current_user)
