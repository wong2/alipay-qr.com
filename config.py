#-*-coding:utf-8-*-

SECRET_KEY = 'THIS IS AN INSECURE SECRET'
UPLOAD_FOLDER = 'qr_images'

WEIBO = dict(
    consumer_key='1575471143',
    consumer_secret='65bd9347098234c912b47922070971c6',
    request_token_params={'scope': 'email'},
    base_url='https://api.weibo.com/2/',
    authorize_url='https://api.weibo.com/oauth2/authorize',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://api.weibo.com/oauth2/access_token',
    content_type='application/json',
)
