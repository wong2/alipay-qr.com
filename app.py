#-*-coding:utf-8-*-

from flask import Flask
from views import index, profile, edit_profile, qr_image


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    register_routes(app)
    return app


def register_routes(app):
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/<username>', 'profile', profile)
    app.add_url_rule('/<username>/edit', 'edit_profile', edit_profile)
    app.add_url_rule('/qr/<username>', 'qr_image', qr_image)


if __name__=='__main__':
    app = create_app()
    app.run('0.0.0.0', debug=True)
