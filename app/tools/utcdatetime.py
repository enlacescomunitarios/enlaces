#-*- coding: utf-8 -*-
#from . import conf as _conf
from datetime import (datetime as _datetime, timedelta as _timedelta)

class _utcDateTime(object):
	def __init__(self, utc='-4'):
		self.utc = int(utc)
		super(_utcDateTime, self).__init__()
	def now(self):
		check = lambda: _datetime.utcnow()-_timedelta(hours=abs(self.utc)) if self.utc<0 else _datetime.utcnow()+_timedelta(hours=abs(self.utc))
		return check()

utc = _utcDateTime()

def to_ddmmyy(o_date):
	return '/'.join(o_date.isoformat().split('-')[::-1])

def to_yymmdd(str_date):
	#y, m, d = str_date.split('/')[::-1]
	#return _datetime.date(int(y), int(m), int(d))
	return '-'.join(str_date.split('/')[::-1])