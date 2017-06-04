import json

from flask import request

from procedures.user_procedure import UserProcedure
from . import auth
from .models import User, Role, init_roles


@auth.route('/user', methods=['POST'])
def register():
    UserProcedure.user_register()


@auth.route('/test')
def test():
    init_roles()
    return 'hello world'
