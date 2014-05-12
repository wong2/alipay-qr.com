#-*-coding:utf-8-*-

from datetime import datetime
from flask_oauthlib.client import OAuth
from redis import Redis
from rq import Queue

from ..config import WEIBO
from ..model import db


q = Queue(connection=Redis())

oauth = OAuth()
weibo = oauth.remote_app('weibo', **WEIBO)


def update_profile(username):
    redis_key = 'users:profile:%s' % username
    access_token, uid = db.hmget(redis_key, 'access_token', 'uid')
    if not access_token:
        return

    @weibo.tokengetter
    def get_weibo_oauth_token():
        return access_token

    user = weibo.get('users/show.json', data={'uid': uid}) 
    user_data = user.data
    if not user_data:
        return

    db.hmset(redis_key, {
        'weibo_name': user_data['name'],
        'weibo_id': user_data['profile_url'],
        'weibo_location': user_data['location'],
        'weibo_avatar': user_data['profile_image_url']
    })


def main():
    splitter = 24 / 2 # two chances every day
    hour = datetime.now().hour % splitter
    uid_to_name_map = db.hgetall('users:lookup:username')
    for uid, username in uid_to_name_map.iteritems():
        if uid % splitter == hour:
            q.enqueue(update_profile, username)


if __name__ == '__main__':
    main()
