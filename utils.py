from enum import Enum


def init_object_from_dict(object, dict):
    """将dict中的值初始化到object中

    dict中包含多余的（object没有的属性）将返回错误
    :param object:  待初始化的对象
    :param dict:
    :return: {code, message, data}
    """
    if object is None:
        return {'code': Status.failed.value, 'message': 'None exception'}
    for key in dict:
        if hasattr(object, key):
            setattr(object, key, dict[key])
        else:
            return {'code': Status.failed.value, 'message': 'parameter include invalid attribute: ' + key}
    return {'code': Status.ok.value, 'message': 'ok', 'data': object}


class Status(Enum):
    ok = 200  # 成功
    failed = 400  # 失败
    not_found = 404  # 资源未找到
    forbidden = 403  # 没有权限
