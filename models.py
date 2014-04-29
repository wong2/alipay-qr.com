#-*-coding:utf-8-*-

from flask.ext.user import UserMixin
from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    real_name = db.Column(db.String(20))
    introduction = db.Column(db.String(500), default='')
    qr_image_key = db.Column(db.String(30), nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean(), nullable=False, default=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')
    email = db.Column(db.String(255), nullable=False, unique=True)
    user_profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    user_profile = db.relationship('UserProfile', uselist=False, foreign_keys=[user_profile_id])


