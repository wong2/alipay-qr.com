#-*-coding:utf-8-*-

from datetime import datetime
from redis import Redis
from rq import Queue

from model import db
from scripts.jobs import update_profile


q = Queue('alipay', connection=Redis())


def main():
    splitter = 24 / 2 # two chances every day
    hour = datetime.now().hour % splitter
    uid_to_name_map = db.hgetall('users:lookup:username')
    for uid, username in uid_to_name_map.iteritems():
        if int(uid) % splitter == hour:
            q.enqueue(update_profile, username)


if __name__ == '__main__':
    main()
