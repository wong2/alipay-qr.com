#-*-coding:utf-8-*-

SECRET_KEY = ''
UPLOAD_FOLDER = 'qr_images' # inside ./static/
STATIC_PREFIX = '/static'

REDIS_URL = 'redis://localhost:6379/5'

WEIBO_KEY  = ''
WEIBO_SECRET = ''

try:
    from local_config import *
except:
    pass
