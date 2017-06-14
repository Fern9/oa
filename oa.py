from flask import Flask
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from auth import auth as blue_auth
from process.views import process as blue_process
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = MongoEngine(app)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)
app.register_blueprint(blue_auth, url_prefix='/api')
app.register_blueprint(blue_process, url_prefix='/process')

app.session_interface = MongoEngineSessionInterface(db)

if __name__ == '__main__':
    app.run(debug=True)
