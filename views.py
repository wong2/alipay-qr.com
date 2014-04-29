#-*-coding:utf-8-*-

from flask import redirect, render_template, url_for


def index():
    if current_user.is_authenticated():
        return redirect(url_for('profile', username=current_user.username))
    else:
        return render_template('create.html')


def profile(username):
    return render_template('profile.html')


@login_required
def edit_profile(username):
    return render_template('edit.html')


def qr_image(username):
    pass
