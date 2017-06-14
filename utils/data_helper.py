# coding=utf-8
from models import Role, Permission
from utils.display_helper import Status


class DataHelper:
    @classmethod
    def init_object_from_dict(cls, obj, attr):
        """将dict中的值初始化到object中

        :param obj:  待初始化的对象
        :param attr:  属性字典
        :return: {code, message, data}
        """
        if object is None:
            return Status.failed, u'None exception', None
        if attr is None:
            return Status.ok, u'ok', obj
        for key in attr:
            if hasattr(obj, key):
                setattr(obj, key, attr[key])
            else:
                pass
                # return Status.failed, u'parameter include invalid attribute: ' + key, None
        return Status.ok, u'ok', obj

    @classmethod
    def mongoset_to_dict(cls, mongoset):
        return [ob.to_mongo().to_dict() for ob in mongoset]

    @classmethod
    def init_roles(cls):
        """初始化角色信息
        :return: no return
        """
        for role in Role.objects.all():
            role.delete()
        common = Role(name="normal", permission=[Permission.APPLY_REQUIRE], default=True)
        repairer = Role(name="repair", permission=[Permission.APPLY_REQUIRE, Permission.EDIT_REPIRE_FORM],
                        default=False)
        admin = Role(name="admin", permission=[Permission.APPLY_REQUIRE, Permission.EDIT_REPIRE_FORM,
                                               Permission.AUTH_ROLE,
                                               Permission.MANAGE_USER], default=False)
        common.save()
        repairer.save()
        admin.save()
