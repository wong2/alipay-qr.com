#-*-coding:utf-8-*-

from flask_oauthlib.client import OAuth

from config import WEIBO
from model import db


oauth = OAuth()
weibo = oauth.remote_app('weibo', **WEIBO)

def change_weibo_header(uri, headers, body):
    """Since weibo is a rubbish server, it does not follow the standard,
    we need to change the authorization header for it."""
    auth = headers.get('Authorization')
    if auth:
        auth = auth.replace('Bearer', 'OAuth2')
        headers['Authorization'] = auth
    return uri, headers, body

weibo.pre_request = change_weibo_header


def update_profile(username):
    redis_key = 'users:profile:%s' % username
    access_token, uid = db.hmget(redis_key, 'access_token', 'uid')
    if not access_token:
        return

    access_token = {'access_token': access_token}
    user = weibo.get('users/show.json', data={'uid': uid}, token=access_token) 
    user_data = user.data

    db.hmset(redis_key, {
        'weibo_name': user_data['name'],
        'weibo_id': user_data['profile_url'],
        'weibo_location': user_data['location'],
        'weibo_avatar': user_data['profile_image_url']
    })


if __name__ == '__main__':
    update_profile('wong2')
