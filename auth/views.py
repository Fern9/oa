import flask
from flask import request
from mongoengine import ValidationError

from .models import User, Role
from . import auth
from utils import init_object_from_dict


@auth.route('/user', methods=['POST'])
def register():
    user = User()
    user = init_object_from_dict(user, request.json)

    if user is None:
        return [code]

    try:
        user.save()
    except ValidationError as e:
        return str(e.message)
    return 'success'


@auth.route('/test')
def test():
    print(User.objects(name='陈酱').first().role.name)
    return 'hello world'
