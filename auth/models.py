from oa import db
import datetime


class User(db.Document):
    title = db.StringField()
    create_time = db.DateTimeField(default=datetime.datetime.now)
