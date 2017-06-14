import json
from models import ProcessDefine
from flask import Blueprint

process = Blueprint('process', __name__)

@process.route('/test')
def test():
    with open('./repair_apply_process_define.json') as json_file:
        define = json.load(json_file)

    process_define = ProcessDefine()
    for key in define:
        if key != 'activities':
            print key
            setattr(process_define, define.get(key))
