from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
instance_path = None


def create_app():
    app = Flask(__name__, static_folder="static")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/cloud'
    app.config['SECRET_KEY'] = 'ej1kl'

    from controller.auth import auth_bp
    from controller.static import static_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(static_bp)

    db.init_app(app)
    login_manager.init_app(app)

    global instance_path
    instance_path = app.instance_path

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
