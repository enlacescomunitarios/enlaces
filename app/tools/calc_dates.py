#-*- coding: utf-8 -*-
#from datetime import date, timedelta
#from . import utcDateTime as _utcDateTime
from . import utc as _utc
from datetime import (date as _date, timedelta as _timedelta)

def to_date(strDate):
	tmpDate = lambda dt: _date(int(dt[0]), int(dt[1]), int(dt[2]))
	return tmpDate(strDate.split('-'))

def _fix_ctrlday(ctrldate):
	return (ctrldate + _timedelta(days=2)) if ctrldate.weekday()==5 else (ctrldate + _timedelta(days=1)) if ctrldate.weekday()==6 else ctrldate

class PreNatal(object):
	weeks_ctrls = [5,16,27,36]
	def __init__(self, y,m,d):
		self.weeks_cal = lambda y,m,d: int(round((_date(y,m,d) - _utc.now().date()).days/7.))
		self.year, self.month, self.day = y, m, d
		assert(self.checking())
		super(PreNatal, self).__init__()
	def checking(self):
		pp = _date(self.year, self.month, self.day)
		days_left = (pp - _utc.now().date()).days
		days_checked = (pp - (pp - _timedelta(days=280))).days
		return True if 0<days_left<=days_checked else False
	def controls_dates(self):
		week = self.weeks_cal(self.year, self.month, self.day) - 4
		weeks = list()
		if week>0:
			weeks += [(4, week, self.fix_ctrlday(week))]
			for i in range(4,1,-1):
				week -= (self.weeks_ctrls[i-1] - self.weeks_ctrls[i-2])
				if week > 0:
					weeks += [(i-1, week, self.fix_ctrlday(week))]
				else:
					break
		return weeks
	def fix_ctrlday(self, week):
		t_day = _utc.now().date() + _timedelta(days=week*7)
		return t_day - _timedelta(days=1) if t_day.weekday()==5 else t_day + _timedelta(days=1) if t_day.weekday()==6 else t_day

class PostNatal(object):
	days_ctrls = [3,7,20,28]
	def __init__(self, y,m,d):
		self.days_calc = lambda: [_fix_ctrlday(_date(y,m,d) + _timedelta(days=i)) for i in self.days_ctrls]
		super(PostNatal, self).__init__()
	def controls_date(self):
		controls = [(cn,dt) for cn,dt in enumerate(self.days_calc(),1) if _utc.now().date()<dt]
		assert(len(controls))
		return controls

class PrePromotional(object):
	weeks_ctrls = [9,15,20,25,30,35]
	def __init__(self, y,m,d):
		self.weeks_calc = lambda: [_fix_ctrlday(_date(y,m,d) + _timedelta(weeks=i)) for i in self.weeks_ctrls]
		super(PrePromotional, self).__init__()
	def controls_date(self):
		controls = [(cn,dt) for cn,dt in enumerate(self.weeks_calc(),1) if _utc.now().date()<dt]
		assert(len(controls))
		return controls

class PostPromotional(object):
	days_ctrls = [3,7,20,28]
	def __init__(self, y,m,d):
		self.days_calc = lambda: [_fix_ctrlday(_date(y,m,d) + _timedelta(days=i)) for i in PostPromotional.days_ctrls]
		super(PostPromotional, self).__init__()
	def controls_date(self):
		controls = [(cn,dt) for cn,dt in enumerate(self.days_calc(),1) if _utc.now().date()<dt]
		assert(len(controls))
		return controls

if __name__ == '__main__':
	days = [u'Lunes',u'Martes',u'Miercoles',u'Jueves',u'Viernes',u'Sábado',u'Domingo']
	y,m,d = input('>>> ')
	a = PreNatal(y,m,d)
	for ctrl in a.controls_dates()[::-1]:
		print u'control: {:2}, semana: {:2}, fecha: {}, día: {}'.format(ctrl[0],ctrl[1],ctrl[2].isoformat(),days[ctrl[2].weekday()])