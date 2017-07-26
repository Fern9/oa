# coding:utf-8
# 配置活动详情页面中的字段显示，编辑状态，是否必填，按钮选项

from models import InstanceStatus

wait = InstanceStatus.wait
running = InstanceStatus.running
repair_page = {
    "default": {
        "show": ["trouble_thing", "address", "phone", "description", "comment"],
        "edit": [],
        "required": [],
        "button": [
            {
                "text": "确定",
                "action": "none"
            }
        ]
    },
    "发起申请": {
    },
    "维修员接单": {
        wait: {
            "repair": {
                "show": ["trouble_thing", "address", "phone", "description", "comment"],
                "edit": [],
                "required": [],
                "button": [
                    {
                        "text": "抢单",
                        "action": "finish"
                    }
                ]
            }
        },
        running: {
            "repair": {
                "show": ["trouble_thing", "address", "phone", "description", "comment"],
                "edit": ["trouble_thing", "description", "comment"],
                "required": ["trouble_thing"],
                "button": [
                    {
                        "text": "确认并开始维修",
                        "action": "finish"
                    }
                ]
            }

        }
    },
    "维修员维修并反馈，填写工时": {
        running: {
            "repair": {
                "show": ["trouble_thing", "address", "phone", "description", "comment", "repair_time", "repair_count"],
                "edit": ["trouble_thing", "description", "comment", "repair_time", "repair_count"],
                "required": ["repair_time"],
                "button": [
                    {
                        "text": "维修完成",
                        "action": "finish"
                    }
                ]
            }
        }
    },
    "用户确认维修结果并付款": {
        running: {
            "repair": {
                "show": ["trouble_thing", "address", "phone", "description", "comment", "repair_count"],
                "edit": [],
                "required": [],
                "button": [
                    {
                        "text": "确认完成",
                        "action": "finish"
                    },
                    {
                        "text": "反馈",
                        "action": ""
                    }
                ]
            }

        }
    },
    "管理员确认": {
        running: {
            "repair": {
                "show": ["trouble_thing", "address", "phone", "description", "comment", "repair_count"],
                "edit": [],
                "required": [],
                "button": [
                    {
                        "text": "确认",
                        "action": "finish"
                    }
                ]
            }
        }
    }
}
