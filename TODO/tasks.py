#coding:utf-8
from celery.decorators import task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
import time
from common import DBActionMYSQL
import os
import datetime

@periodic_task(run_every=datetime.timedelta(hours=1, minutes=1, seconds=1))
# @periodic_task(run_every=crontab())
def timer_scrapy_news():
	db = DBActionMYSQL()
	r = db.delete()
	os.system("cd /root/various; scrapy crawl ifeng")
