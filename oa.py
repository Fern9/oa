from flask import Flask
from flask_mongoengine import MongoEngineSessionInterface
from auth.views import auth as blue_auth
from process.views import process
from models import db
from auth.procedures.login_procedure import login_manager

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
app.register_blueprint(blue_auth, url_prefix='/api/auth')
app.register_blueprint(process, url_prefix='/api/process')
login_manager.init_app(app)

app.session_interface = MongoEngineSessionInterface(db)


if __name__ == '__main__':
    app.run(debug=True)
