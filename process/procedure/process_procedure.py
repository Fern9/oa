# coding:utf-8
import json
import os

from flask import session

import settings
from flask_login import current_user
from models import ProcessDefine, ActivityDefine, ProcessInst, User, ActivityInst, InstanceStatus, Participant
from utils.display_helper import Status
from auth.procedures.user_procedure import UserProcedure

class Process():
    def __init__(self):
        pass

    @classmethod
    def init_process_define(cls):
        json_file_path = os.path.join(settings.APP_PATH, 'process/repair_apply_process_define.json')
        with open(json_file_path) as json_file:
            define = json.load(json_file)
        for obj in ProcessDefine.objects().all():
            obj.delete()
        process_define = ProcessDefine()
        for key in define:
            if key != 'activities':
                setattr(process_define, key, define.get(key))
        activities = define.get('activities')
        for activity in activities:
            activity_define = ActivityDefine()
            for key in activity:
                if key != 'participants':
                    setattr(activity_define, key, activity.get(key))
                else:
                    par_temp = activity.get('participants')
                    participant = Participant(type=par_temp['type'], value=par_temp['value'])
                    activity_define.participants = participant
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
        process_instance.state = InstanceStatus.running
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
                is_start = False
                activity_inst.save()
                process_instance.curr_activity = activity_inst
                process_instance.save()

            activity_inst.save()
        return Status.ok, u'ok', {'id': process_instance.id}

    @classmethod
    def finish_curr_activity_start_next(cls, process_inst_id):
        """
        结束流程当前环节并开始下一环节
        :param process_inst_id:
        :return:
        """
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
            process_instance.curr_activity = None
            process_instance.save()
        else:
            if next_activity.activity_define.direct_active:
                next_activity.state = InstanceStatus.running
                if next_activity.activity_define.participants.type == 'role':
                    next_activity.participants.append(next_activity.activity_define.participants)
                elif next_activity.activity_define.participants.type == 'front':
                    front_value = next_activity.activity_define.participants.value
                    next_activity.participants = activities[front_value - 1].participants
            else:
                next_activity.state = InstanceStatus.wait
            # next_activity.form = curr_activity.form
            next_activity.save()
            process_instance.curr_activity = next_activity
            process_instance.save()
        return Status.ok, u'ok', None

    @classmethod
    def run_activity(cls, activity_id, user=current_user):
        activity = ActivityInst.objects().get(id=activity_id)
        if activity.state == InstanceStatus.wait:
            activity.state = InstanceStatus.running
            participant = Participant(type='user', value=user.id)
            activity.participants.append(participant)
        elif activity.state == InstanceStatus.block:
            activity.state = InstanceStatus.running
        else:
            return Status.failed, u'该活动不能激活', None
        activity.save()
        return Status.ok, u'ok', None

    @classmethod
    def get_wait_activities(cls, user=current_user):
        """
        获取待领取的任务
        :param user:
        :return:
        """
        if user.role.name != 'admin':
            activities = ActivityInst.objects(activity_define__participants__value=user.role.name,
                                              state=InstanceStatus.wait).all()
        else:
            activities = ActivityInst.objects(state=InstanceStatus.wait).all()
        processes = cls.get_process_by_activities(activities)
        return Status.ok, u'ok', processes

    @classmethod
    def get_running_activities(cls, user=current_user):
        """
        获取前用户正在运行的活动
        :param user:
        :return:
        """
        activities = ActivityInst.objects.filter(participants__value__in=['normal', str(user.id)],
                                                 state=InstanceStatus.running).all()

        processes = cls.get_process_by_activities(activities)
        return Status.ok, u'ok', processes


    @classmethod
    def get_running_start_by(cls, user=current_user):
        """
        获取有用户发起的并且当前流程正在运行的活动
        :param user:
        :return:
        """
        process_inst = ProcessInst.objects(state=InstanceStatus.running)
        activities = ActivityInst.objects.filter(participants__value__in=[str(user.id)], sequence=1,
                                                 process_inst__in=process_inst)
        processes = cls.get_process_by_activities(activities)
        return Status.ok, u'ok', processes



    @classmethod
    def get_end_history(cls, user=current_user):
        """获取用户参与的已经结束的流程"""
        activities = ActivityInst.objects.filter(participants__value__in=[str(user.id)])
        process_id_list = set()
        for activity in activities:
            process_id_list.add(activity.process_inst.id)
        processes = ProcessInst.objects.filter(id__in=process_id_list, state=InstanceStatus.dead)
        return Status.ok, u'ok', processes

    @classmethod
    def get_all_history(cls, user=current_user):
        """获取用户参与的所有流程"""
        activities = ActivityInst.objects.filter(participants__value__in=[str(user.id)])
        process_id_list = set()
        for activity in activities:
            process_id_list.add(activity.process_inst.id)
        processes = ProcessInst.objects.filter(id__in=process_id_list)
        return Status.ok, u'ok', processes

    @classmethod
    def update_form(cls,process_id, form):
        process_inst = ProcessInst.objects(id=process_id)
        if process_inst is None:
            return Status.not_found, u'failed', None
        for key in form:
            process_inst.form[key] = form[key]
        process_inst.save()
        return Status.ok, u'ok', None

    @classmethod
    def get_wait_order(cls, user=current_user):
        """待接单
        :param user:
        :return:
        """
        activities = ActivityInst.objects.filter(participants__value__in=[str(user.id)], sequence=1)
        processes = set()
        for activity in activities:
            if activity.process_inst.curr_activity.state == InstanceStatus.wait:
                processes.add(activity.process_inst)
        return Status.ok, u'ok', processes

    @classmethod
    def get_wait_repair(cls, user=current_user):
        """待修理
        :param user:
        :return:
        """
        activities = ActivityInst.objects.filter(participants__value__in=[str(user.id)], sequence=1)
        processes = set()
        for activity in activities:
            if activity.process_inst.curr_activity.state == InstanceStatus.running:
                processes.add(activity.process_inst)
        return Status.ok, u'ok', processes

    @classmethod
    def get_process_by_activities(cls, activities):
        """
        传入活动列表，返回对应的流程列表
        :param activities:
        :return:
        """
        processes = set()
        for activity in activities:
            processes.add(activity.process_inst)
        return processes

    @classmethod
    def get_process_data(cls, process_id):
        process = ProcessInst.objects(id=process_id).first()
        if process is None:
            return Status.not_found, u'未找到流程信息', None
        data = dict()
        data['process_data'] = process
        data['curr_data'] = process.curr_activity
        data['curr_participants'] = UserProcedure.participants_to_users(process.curr_activity.participants)
        return Status.ok, 'ok', data


