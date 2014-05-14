#-*-coding:utf-8-*-

import os
import re
import model
from functools import wraps
from hashlib import sha1
from flask import (Flask, redirect, render_template, url_for,
        request, session, abort, g, jsonify, flash)
from weibo_oauth import weibo, oauth

app = Flask(__name__)
app.config.from_object('config')


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


def get_all_endpoints():
    fn = get_all_endpoints
    if not fn.endpoints:
        fn.endpoints = [
            rule.endpoint for rule in app.url_map.iter_rules()
        ]
    return fn.endpoints

get_all_endpoints.endpoints = []


def is_username_valid(username):
    if len(username) > 20:
        return False
    if username in get_all_endpoints():
        return False
    if model.username_exists(username):
        return False
    if not re.match('^[a-zA-Z0-9_]+$', username):
        return False
    return True


@app.route('/')
def index():
    if 'oauth_token' in session:
        if not g.username:
            return redirect(url_for('create_profile'))
        else:
            return redirect(url_for('profile', username=g.username))
    else:
        return render_template('login.html')


def validate(username, realname, intro, file):
    if not is_username_valid(username):
        return u'用户名不合法'
    if len(intro) > 300:
        return u'自我介绍不能超过300个字符'
    if not file:
        return u'请选择文件'
    if not is_allowed_file(file.filename):
        return u'请选择图片文件'


@app.route('/create', methods=['GET', 'POST'])
@require_login
def create_profile():
    uid = session['uid']
    username = realname = intro = ''
    if request.method == 'POST':
        username = request.form.get('username')
        realname = request.form.get('realname', '')
        intro = request.form.get('intro', '')
        file = request.files.get('qr_image', None)
        
        error = validate(username, realname, intro, file)
        if not error:
            filename = '%s.jpg' % sha1(username).hexdigest()
            file.save(os.path.join('static', app.config['UPLOAD_FOLDER'], filename))

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
            flash(u'创建成功，把这个网页分享给好友就可以了~', category='success')
            return redirect(url_for('profile', username=username))
        else:
            flash(error, category='danger')

    user = weibo.get('users/show.json', data={'uid': uid})
    payload = user.data
    payload.update({
        'username': username,
        'realname': realname,
        'intro': intro
    })
    return render_template('create.html', **user.data)


@app.route('/check', methods=['GET', 'POST'])
def check_username():
    username = request.values['username']
    return jsonify({
        'valid': is_username_valid(username)
    })


@app.route('/<username>')
def profile(username):
    profile = model.get_profile(username)
    is_owner = g.username == username
    if not profile:
        abort(404)
    return render_template('profile.html', is_owner=is_owner, **profile)


@app.route('/<username>/edit', methods=['POST'])
@require_login
def edit(username):
    if g.username != username:
        abort(403)
    new_intro = request.form['intro']
    model.update_profile(g.username, intro=new_intro)
    return 'ok'


@app.route('/qr/<username>')
def qr_image(username):
    image_name = model.get_qr_image(username)
    return redirect('%s/%s/%s' % (app.config['STATIC_PREFIX'],
        app.config['UPLOAD_FOLDER'], image_name))


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
