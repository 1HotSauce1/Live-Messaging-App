from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session

database = SQLAlchemy()
DATABASE_USERNAME = 'postgres'
DATABASE_PASSWORD = 'dragospass'
DATABASE_NAME = 'postgres'

def create_app():
    app = Flask(__name__)
    # must change SECRET_KEY
    app.config['SECRET_KEY'] = 'asdadad'
    app.config['SESSION_TYPE'] = 'filesystem'

    # Views / Routing
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@localhost:5432/{}'.format(DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_NAME)
    database.init_app(app)

    # Login manager
    from .models import User_profiles
    
    login_manager = LoginManager()
    login_manager.login_view = 'views.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User_profiles.query.get(int(id))

    # Server side session
    server_session = Session()
    server_session.init_app(app)

    return app