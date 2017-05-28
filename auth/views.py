import flask
from .models import User
from . import auth


@auth.route('/user', methods=['PUT'])
def register():
    user = User(title='test_title')
    user.save()
    return 'success'

@auth.route('/test')
def test():
    return 'hello world'
