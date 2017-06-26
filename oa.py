from flask import Flask
from flask_mongoengine import MongoEngineSessionInterface
from auth.views import auth as blue_auth
from process.views import process
from models import db
from auth.procedures.login_procedure import login_manager
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
app.register_blueprint(blue_auth, url_prefix='/api/auth')
app.register_blueprint(process, url_prefix='/api/process')
login_manager.init_app(app)

app.session_interface = MongoEngineSessionInterface(db)
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)



if __name__ == '__main__':
    # app.run(debug=True)
    IOLoop.instance().start()