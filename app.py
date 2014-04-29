#-*-coding:utf-8-*-

from flask import (Flask, redirect, render_template, url_for,
        request, session)
from flask_oauthlib.client import OAuth


app = Flask(__name__)
app.config.from_object('config')

oauth = OAuth()
weibo = oauth.remote_app('weibo', app_key='WEIBO')
oauth.init_app(app)


@app.route('/')
def index():
    if 'uid' in session:
        access_token = session['oauth_token'][0]
        uid = session['uid']
        created = False
        if not created:
            user = weibo.get('users/show.json', data={'uid': uid})
            return render_template('create.html', **user.data)
        else:
            return redirect(url_for('profile', username='wong2'))
    else:
        return render_template('login.html')


@app.route('/<username>')
def profile(username):
    return render_template('profile.html')


@app.route('/<username>/edit')
def edit_profile(username):
    return render_template('edit.html')


@app.route('/qr/<username>')
def qr_image(username):
    pass


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login')
def login():
    return weibo.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('oauth_token', None)
    session.pop('uid', None)
    return redirect(url_for('index'))


@app.route('/login/authorized')
@weibo.authorized_handler
def authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    session['uid'] = resp['uid']
    return redirect(url_for('index'))


@weibo.tokengetter
def get_weibo_oauth_token():
    return session.get('oauth_token')


def change_weibo_header(uri, headers, body):
    """Since weibo is a rubbish server, it does not follow the standard,
    we need to change the authorization header for it."""
    auth = headers.get('Authorization')
    if auth:
        auth = auth.replace('Bearer', 'OAuth2')
        headers['Authorization'] = auth
    return uri, headers, body

weibo.pre_request = change_weibo_header


if __name__=='__main__':
    app.run('0.0.0.0', debug=True)
