import datetime
from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_pyfile('the-config.cfg')

db = MongoEngine(app)

class Todo(db.Document):
    title = db.StringField(max_length=60)
    text = db.StringField()
    done = db.BooleanField(default=False)
    pub_date = db.DateTimeField(default=datetime.datetime.now)

@app.route('/')
def index():
    # As a list to test debug toolbar
    Todo.objects().delete()  # Removes
    Todo(title="Simple todo B ПЫЩЬ!", text="12345678910").save()  # Insert
    Todo(title="Simple todo B", text="12345678910").save()  # Insert
    Todo.objects(title__contains="B").update(set__text="Hello world")  # Update
    todos = Todo.objects.all()
    return 'hello world'



if __name__ == '__main__':
    app.run()
