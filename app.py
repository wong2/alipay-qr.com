#-*-coding:utf-8-*-

import os
import model
from functools import wraps
from hashlib import sha1
from flask import (Flask, redirect, render_template, url_for, request, session, abort, g, send_from_directory, jsonify)
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.config.from_object('config')

oauth = OAuth()
weibo = oauth.remote_app('weibo', app_key='WEIBO')
oauth.init_app(app)


@app.before_request
def before_request():
    uid = session.get('uid')
    g.username = model.get_username(uid)
    g.uid = uid


def require_login(f):
    @wraps(f)
    def _(*args, **kwargs):
        if 'oauth_token' not in session:
            return redirect(url_for('index'))
        else:
            return f(*args, **kwargs)
    return _

def is_allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ['jpg', 'jpeg','png']


@app.route('/')
def index():
    if 'oauth_token' in session:
        if not g.username:
            uid = session['uid']
            user = weibo.get('users/show.json', data={'uid': uid})
            return render_template('create.html', **user.data)
        else:
            return redirect(url_for('profile', username=g.username))
    else:
        return render_template('login.html')


@app.route('/create', methods=['POST'])
@require_login
def create_profile():
    uid = session['uid']
    username = request.form.get('username')
    realname = request.form.get('realname', '')
    intro = request.form.get('intro', '')

    file = request.files['qr_image']
    if file and is_allowed_file(file.filename):
        filename = '%s.jpg' % sha1(username).hexdigest()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    user = weibo.get('users/show.json', data={'uid': uid})
    user_data = user.data

    access_token, _ = session['oauth_token']
    profile = {
        'uid': uid,
        'access_token': access_token,
        'username': username,
        'realname': realname,
        'intro': intro,
        'qr_image': filename,
        'weibo_name': user_data['name'],
        'weibo_id': user_data['profile_url'],
        'weibo_location': user_data['location'],
        'weibo_avatar': user_data['profile_image_url'],
    }
    model.create_profile(uid, username, profile)
    return redirect(url_for('profile', username=username))


@app.route('/check', methods=['GET', 'POST'])
def check_username():
    username = request.values['username']
    return jsonify({
        'valid': not model.username_exists(username)
    })


@app.route('/<username>')
def profile(username):
    profile = model.get_profile(username)
    is_owner = g.username == username
    if not profile:
        abort(404)
    return render_template('profile.html', is_owner=is_owner, **profile)


@app.route('/edit', methods=['POST'])
@require_login
def edit():
    new_intro = request.form['intro']
    model.update_profile(g.username, intro=new_intro)
    return 'ok'


@app.route('/qr/<username>')
def qr_image(username):
    image_name = model.get_qr_image(username)
    return send_from_directory(app.config['UPLOAD_FOLDER'], image_name)


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
