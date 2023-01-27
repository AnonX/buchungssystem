from flask import Flask
# Flask initialisieren und den Secret Key bestimmen
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abc'

    from .view import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app