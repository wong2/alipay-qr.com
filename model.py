#-*-coding:utf-8-*-

from redis import StrictRedis

db = StrictRedis(decode_responses=True)


def create_profile(uid, username, profile):
    db.hmset('users:profile:%s' % username, profile)
    db.hset('users:lookup:username', uid, username)


def get_profile(username):
    return db.hgetall('users:profile:%s' % username)


def get_qr_image(username):
    return db.hget('users:profile:%s' % username, 'qr_image')


def get_username(uid):
    if not uid:
        return
    return db.hget('users:lookup:username', uid)

def username_exists(username):
    return db.exists('users:profile:%s' % username)
