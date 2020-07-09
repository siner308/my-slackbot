# coding: utf-8
from __future__ import unicode_literals
import pymongo
import datetime
from functions.decorators import on_command
from gevent.monkey import patch_all
from slack import slack_notify

from settings import MONGO_HOST, MONGO_PORT, MONGO_DATABASE, BOT_NAME, CHANNEL

patch_all()


@on_command(['ㅊㅋ'])
def run(robot, channel, user, tokens):
    fallback = '출퇴근봇알리미'
    attachments_dict = dict()

    dbclient = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
    db = dbclient[MONGO_DATABASE]
    coll = db['commute']

    key = {"user": user}
    rows = list(coll.find(key).sort('_id', pymongo.DESCENDING))

    if not len(rows):
        text = '출퇴근 이력이 없습니다. 입사하세요'
    else:
        data = rows[0]

        try:
            worktime = data['worktime']
        except:
            worktime = None

        if worktime is not None:
            text = "[%s] ~ [%s]\n총 근무시간 : `%s`" % (data['start_time'], data['end_time'], worktime)
        else:
            text = "`%s`에 출근했습니다." % data['start_time']

    attachments_dict['fallback'] = fallback
    attachments_dict['text'] = text
    attachments = [attachments_dict]
    slack_message = None
    slack_notify(text=slack_message, channel=CHANNEL, username=BOT_NAME, attachments=attachments)
