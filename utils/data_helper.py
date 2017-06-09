# coding=utf-8
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
