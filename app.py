#-*-coding:utf-8-*-

from flask import Flask, request
from flask.ext.babel import Babel
from flask.ext.mail import Mail
from flask.ext.user import UserManager, SQLAlchemyAdapter

from models import db, User, UserProfile
from views import index, profile, edit_profile, qr_image


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    register_database(app)
    register_babel(app)
    register_user(app)
    register_routes(app)
    Mail(app)

    return app


def register_database(app):
    db.init_app(app)
    db.app = app
    db.create_all()


def register_babel(app):
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        translations = [str(t) for t in babel.list_translations()]
        return request.accept_languages.best_match(translations)


def register_user(app):
    db_adapter = SQLAlchemyAdapter(db, UserClass=User, UserProfileClass=UserProfile)
    UserManager(db_adapter, app)


def register_routes(app):
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/<username>', 'profile', profile)
    app.add_url_rule('/<username>/edit', 'edit_profile', edit_profile)
    app.add_url_rule('/qr/<username>', 'qr_image', qr_image)


if __name__=='__main__':
    app = create_app()
    app.run('0.0.0.0', debug=True)
