from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Vit@delaris@05'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://train_app_d7hh_user:gqrWx3nSB1dT1ML7zUsYa083ImDo7yiT@dpg-d0s9ki3ipnbc73eprh4g-a.frankfurt-postgres.render.com/train_app_d7hh'

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, City, Route

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app


def create_database(app_):
    with app_.app_context():
        db.create_all()
    print('Ensured tables exist in the PostgreSQL database!')

# def create_database(app_):
#     if not path.exists('website/' + DB_NAME):
#         with app_.app_context():
#             db.create_all()
#         print('Created Database!')
#     else:
#         print('Database already exists.')