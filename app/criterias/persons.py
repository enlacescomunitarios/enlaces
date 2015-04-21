#-*- coding: utf-8 -*-
from __future__ import absolute_import
from pony.orm import (db_session as _db_session, select as _select)
from ..entities import (Persona as _Persona,)

class PersonCriteria:
	@classmethod
	def v_ci(self, ci):
		try:
			with _db_session:
				return _select(pr for pr in _Persona if pr.ci==ci).exists()
		except Exception, e:
			#raise e
			return False
	@classmethod
	def v_telf(self, telf):
		try:
			with _db_session:
				return _select(pr for pr in _Persona if pr.telf==telf).exists()
		except Exception, e:
			#raise e
			False