#-*-coding:utf-8-*-

SECRET_KEY = 'THIS IS AN INSECURE SECRET'               # Change this for production!!!
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'  # Use Sqlite file db
CSRF_ENABLED = True

# Configure Flask-Mail -- Required for Confirm email and Forgot password features
MAIL_SERVER   = 'smtp.gmail.com'
MAIL_PORT     = 465
MAIL_USE_SSL  = True                            # Some servers use MAIL_USE_TLS=True instead
MAIL_USERNAME = 'wonderfuly@gmail.com'
MAIL_PASSWORD = 'w)nderfu1y'
MAIL_DEFAULT_SENDER = '"Sender" <noreply@alipay-qr.com>'

# Configure Flask-User
USER_ENABLE_USERNAME         = True
USER_ENABLE_CONFIRM_EMAIL    = True
USER_ENABLE_CHANGE_USERNAME  = False
USER_ENABLE_CHANGE_PASSWORD  = False
USER_ENABLE_FORGOT_PASSWORD  = False
USER_ENABLE_RETYPE_PASSWORD  = True
USER_LOGIN_TEMPLATE = 'login.html'
USER_REGISTER_TEMPLATE = 'register.html'

# qiniu
Q_ACCESS_TOKEN = 'eYy9jQlxRSftSS9Cp52gJvZ7BoIQWsfVa0lNqGzS'
Q_SECRET_TOKEN = '0_bJt39r7Fb19AJDt6kl0defsW72wFfVV8X_42yf'
Q_BUCKET = 'alipay-qr'
Q_DOMAIN = '{bucket}.qiniudn.com'.format(bucket=Q_BUCKET)
