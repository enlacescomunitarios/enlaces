#-*- coding: utf-8 -*-
from __future__ import absolute_import
from ..tools import getLocals
from pony.orm import (db_session as _db_session, commit as _commit, select as _select, count as _count)
from ..entities import (Recien_Nacido as _newBorn, Defuncion as _Death)

class ChildrensCriteria:
	@classmethod
	def total_childrens(self):
		return _count(ch for ch in _newBorn)
	@classmethod
	def death(self, id_rcn, fecha, f_notf, obs_notf, f_conf=None, obs_conf=None):
		deathForm = getLocals(locals())
		try:
			with _db_session:
				child = _newBorn.get(id_rcn=id_rcn)

		except Exception, e:
			raise e