import json
import os

from flask import session

import settings

from models import ProcessDefine, ActivityDefine, ProcessInst, User, ActivityInst
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
        # if 'open_id' not in session:
        #     return Status.unauth, u'need to login', None
        # curr_user = User.objects(wx_open_id=session['open_id']).first()
        # process_instance.creator = curr_user
        for activity in process_define.activities:
            activity_inst = ActivityInst()
            activity_inst.inst_name = activity.define_name
            activity_inst.activity_define = activity
            activity_inst.state = 1
            activity_inst.sequence = activity.sequence
            activity_inst.participants = []
            process_instance.activities.insert(activity_inst.sequence, activity_inst)
        process_instance.activities[0].state = 2
        process_instance.activities[0].participants.append({'type': 'user', 'value': 123})
        process_instance.activities[0].form = form
        process_instance.form = form
        process_instance.save()
        return Status.ok, u'ok', {'id': process_instance.id}

    @classmethod
    def finish_curr_activity_start_next(cls, process_inst_id):
        process_instance = ProcessInst.objects().get(id=process_inst_id)
        curr_index = 0
        for x in process_instance.activities:
            if process_instance.activities[x].state == 2:
                curr_index = x
        process_instance.activities[curr_index].state = 4
        process_instance.activities[curr_index+1].state = 2
