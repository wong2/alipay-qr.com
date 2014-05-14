#-*-coding:utf-8-*-

from model import db
from weibo_oauth import weibo


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
