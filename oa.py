from flask import Flask
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from auth import auth as blue_auth
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile('the-config.cfg')
db = MongoEngine(app)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)
app.register_blueprint(blue_auth, url_prefix='/auth')
app.session_interface = MongoEngineSessionInterface(db)


if __name__ == '__main__':
    app.run(debug=True)


