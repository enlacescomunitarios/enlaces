#-*- coding: utf-8 -*-
from . import conf as _conf
from datetime import (datetime as _datetime, timedelta as _timedelta)

class utcDateTime(object):
	def __init__(self, utc=_conf.timezone.utc):
		self.utc = int(utc)
		super(utcDateTime, self).__init__()
	def now(self):
		check = lambda: _datetime.utcnow()-_timedelta(hours=abs(self.utc)) if self.utc<0 else _datetime.utcnow()+_timedelta(hours=abs(self.utc))
		return check()

def to_ddmmyy(o_date):
	return '/'.join(o_date.isoformat().split('-')[::-1])

def to_yymmdd(str_date):
	#y, m, d = str_date.split('/')[::-1]
	#return _datetime.date(int(y), int(m), int(d))
	return '-'.join(str_date.split('/')[::-1])

if __name__ == '__main__':
	dt = utcDateTime(utc=input('timezone: '))
	print dt.now()