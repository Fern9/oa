import flask
from mongoengine import ValidationError

from .models import User, Role
from . import auth


@auth.route('/user', methods=['PUT'])
def register():
    role = Role.objects(default=True).first()
    print(role)
    wx_user = {'id': '01', 'name': '陈宇航'}
    user = User(wx_user=wx_user, name='陈酱', role=role)
    try:
        user.save()
    except ValidationError as e:
        return e.message

    return 'success'


@auth.route('/test')
def test():
    print(User.objects(name='陈酱').first().role.name)
    return 'hello world'


