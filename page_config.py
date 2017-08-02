# coding:utf-8
# 配置活动详情页面中的字段显示，编辑状态，是否必填，按钮选项

from models import InstanceStatus

wait = InstanceStatus.wait
running = InstanceStatus.running
repair_page = {
    "default": {
        "show": {"trouble_thing": 1, "address": 1, "phone": 1, "description": 1, "comment": 1, "repair_time": 0, "repair_count": 0},
        "edit": {"trouble_thing": 0, "address": 0, "phone": 0, "description": 0, "comment": 0, "repair_time": 0, "repair_count": 0},
        "required": {"trouble_thing": 0, "address": 0, "phone": 0, "description": 0, "comment": 0, "repair_time": 0, "repair_count": 0},
        "button": [
            {
                "text": "确定",
                "action": "no_action"
            }
        ]
    },
    u"发起申请": {
    },
    u"维修员接单": {
        wait: {
            "repair": {
                "show": {"trouble_thing": 1, "address": 1, "phone": 1, "description": 1, "comment": 1, "repair_time": 0, "repair_count": 0},
                "edit": {"trouble_thing": 0, "address": 0, "phone": 0, "description": 0, "comment": 0, "repair_time": 0, "repair_count": 0},
                "required": {"trouble_thing": 0, "address": 0, "phone": 0, "description": 0, "comment": 0, "repair_time": 0, "repair_count": 0},
                "button": [
                    {
                        "text": "抢单",
                        "action": "next"
                    }
                ]
            }
        },
        running: {
            "repair": {
                "show": {"trouble_thing": 1, "address": 1, "phone": 1, "description": 1, "comment": 1, "repair_time": 0, "repair_count": 0},
                "edit": {"trouble_thing": 1, "address": 0, "phone": 0, "description": 1, "comment": 1, "repair_time": 0, "repair_count": 0},
                "required": {"trouble_thing": 1, "address": 0, "phone": 0, "description": 0, "comment": 0, "repair_time": 0, "repair_count": 0},
                "button": [
                    {
                        "text": "保存",
                        "action": "update"
                    },
                    {
                        "text": "确认并开始维修",
                        "action": "next"
                    }
                ]
            }

        }
    },
    u"维修员维修并反馈，填写工时": {
        running: {
            "repair": {
                "show": {"trouble_thing": 1, "address": 1, "phone": 1, "description": 1, "comment": 1, "repair_time": 1, "repair_count": 1},
                "edit": {"trouble_thing": 1, "address": 0, "phone": 0, "description": 1, "comment": 1, "repair_time": 1, "repair_count": 1},
                "required": {"trouble_thing": 1, "address": 0, "phone": 0, "description": 0, "comment": 0, "repair_time": 1, "repair_count": 1},
                "button": [
                    {
                        "text": "保存",
                        "action": "update"
                    },
                    {
                        "text": "维修完成",
                        "action": "next"
                    }
                ]
            }
        }
    },
    u"用户确认维修结果并付款": {
        running: {
            "normal": {
                "show": {"trouble_thing": 1, "address": 1, "phone": 1, "description": 1, "comment": 1, "repair_time": 0, "repair_count": 1},
                "edit": {"trouble_thing": 0, "address": 0, "phone": 0, "description": 0, "comment": 0, "repair_time": 0, "repair_count": 0},
                "required": {"trouble_thing": 0, "address": 0, "phone": 0, "description": 0, "comment": 0, "repair_time": 0, "repair_count": 0},
                "button": [
                    {
                        "text": "确认完成",
                        "action": "next"
                    },
                    {
                        "text": "反馈",
                        "action": "no_action"
                    }
                ]
            }

        }
    },
    u"管理员确认": {
        running: {
            "admin": {
                "show": {"trouble_thing": 1, "address": 1, "phone": 1, "description": 1, "comment": 1, "repair_time": 1, "repair_count": 1},
                "edit": {"trouble_thing": 0, "address": 0, "phone": 0, "description": 0, "comment": 0, "repair_time": 1, "repair_count": 1},
                "required": {"trouble_thing": 0, "address": 0, "phone": 0, "description": 0, "comment": 0, "repair_time": 1, "repair_count": 1},
                "button": [
                    {
                        "text": "确认",
                        "action": "next"
                    }
                ]
            }
        }
    }
}
