import flask, json
from flask import request
from mongoengine import ValidationError
from .models import User, Role, init_roles
from . import auth
from utils import init_object_from_dict, Status


@auth.route('/user', methods=['POST'])
def register():
    user = User()
    result = init_object_from_dict(user, request.json)
    if result['code'] != Status.ok.value:
        return json.dumps(result)
    try:
        user = result['data']
        if 'role' in request.json:
            role = Role.objects(name=request.json['role']).first()
            if role is None:
                return json.dumps(
                    {'code': Status.failed.value, 'message': 'can not find Role: ' + request.json['role']})
        else:
            role = Role.objects(default=True).first()
        user.role = role
        user.save()
    except ValidationError as e:
        return json.dumps({'code': Status.failed.value, 'message': e.message})
    return json.dumps({'code': Status.create.value, 'message': 'ok'})


@auth.route('/test')
def test():
    init_roles()
    return 'hello world'
