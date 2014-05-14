#-*-coding:utf-8-*-

from flask_oauthlib.client import OAuth
from config import WEIBO_KEY, WEIBO_SECRET


WEIBO = dict(
    consumer_key=WEIBO_KEY,
    consumer_secret=WEIBO_SECRET,
    request_token_params={'scope': 'email'},
    base_url='https://api.weibo.com/2/',
    authorize_url='https://api.weibo.com/oauth2/authorize',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://api.weibo.com/oauth2/access_token',
    content_type='application/json',
)

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
