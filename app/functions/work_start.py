# coding: utf-8
from __future__ import unicode_literals
import pymongo
import datetime
from functions.decorators import on_command
from gevent.monkey import patch_all
from slack import slack_notify
from settings import MONGO_HOST, MONGO_PORT, MONGO_DATABASE, BOT_NAME, CHANNEL

patch_all()


@on_command(['출근', '출근!', '출근!!', '출근!!!',
             '일할게', '일할게!', '일할게!!', '일할게!!!',
             'ㅊㄱ', 'ㅊㄱ!', 'ㅊㄱ!!', 'ㅊㄱ!!!'])
def run(robot, channel, user, tokens):
    fallback = '출퇴근봇알리미'
    attachments_dict = dict()

    dbclient = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
    db = dbclient[MONGO_DATABASE]
    coll = db['commute']

    key = {"user": user}
    rows = list(coll.find(key).sort('_id', pymongo.DESCENDING))
    if len(rows):
        data = rows[0]
        try:
            worktime = data['worktime']
        except:
            worktime = None
    else:
        worktime = '첫출근입니다'

    if worktime is None:
        text = "어디서 퇴근도 안하고 출근을!!!"
    else:
        start_time = datetime.datetime.now()
        data = {"user": user, "start_time": start_time}
        try:
            x = coll.insert_one(data)
            text = "[%s] - 출근 - %s" % (str(start_time), x.inserted_id)
        except Exception as e:
            text = str(e)
            fallback = '고장났어!!!'

    attachments_dict['fallback'] = fallback
    attachments_dict['text'] = text
    attachments = [attachments_dict]
    slack_message = None
    slack_notify(text=slack_message, channel=CHANNEL, username=BOT_NAME, attachments=attachments)
