#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template
import datetime
import time

register = template.Library()


@register.tag(name="computing_time")
def computing_time(data, time_left):
	return_str = ""
	fmt = "%Y-%m-%d %H:%M:%S"
	t = time.strptime(data.add_time, fmt)
	t1 = datetime.datetime(*t[:6])
	t2 = datetime.datetime.now()
	tt = (t2 - t1)
	if data.is_complete == "1":
		_t = time.strptime(data.complete_time, fmt)
		t3 = datetime.datetime(*_t[:6])
		tt = (t3 - t1)
	days = tt.days
	seconds = tt.seconds
	total_seconds = int(data.time_day) * 86400 + int(data.time_hours) * 3600 + int(data.time_minute) * 60
	use_seconds = int(days) * 86400 + seconds
	sps_seconds = total_seconds - use_seconds
	sps_day = sps_seconds > 0 and sps_seconds / 86400 or 0
	_str = ""
	if 0 < sps_seconds:
		_str = time.strftime('%H 时 %M 分', time.gmtime(sps_seconds))
		if 0 < sps_day:
			_str = time.strftime('%H 时 %M 分', time.gmtime(sps_seconds - sps_day * 86400))
	else:
		_str = "00 时 00 分"
	if time_left:
		if data.is_complete == "1":
			return_str = "3"
		else:
			if int(sps_seconds) < 0:
				return_str = "2"
			else:
				if int(sps_day) == 0 and int(_str.split(" ")[0]) < 1:
					return_str = "1"
	else:
		return_str = '%s 天' % (sps_day) + _str
	return return_str


register.filter(computing_time)
