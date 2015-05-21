#-*- coding: utf-8 -*-
from __future__ import absolute_import
from ..tools import getLocals
from pony.orm import (db_session as _db_session, select as _select, commit as _commit)
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
	@classmethod
	def update(self, id_per, nombres, apellidos, telf, sexo):
		form = getLocals(locals())
		try:
			with _db_session:
				pr = _Persona.get(id_per=id_per); del form.id_per
				pr.set(**form)
				_commit()
			return True
		except Exception, e:
			raise e
			return False