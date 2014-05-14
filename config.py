#-*-coding:utf-8-*-

SECRET_KEY = 'THIS IS AN INSECURE SECRET'
UPLOAD_FOLDER = 'qr_images' # inside ./static/
STATIC_PREFIX = '/static'

REDIS_URL = 'redis://localhost:6379/5'

WEIBO_KEY  = '1575471143'
WEIBO_SECRET = '65bd9347098234c912b47922070971c6'

try:
    from local_config import *
except:
    pass
