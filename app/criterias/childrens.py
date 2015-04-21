#-*- coding: utf-8 -*-
from __future__ import absolute_import
from pony.orm import (db_session as _db_session, commit as _commit, select as _select, count as _count)
from ..entities import (Recien_Nacido as _newBorn,)

class ChildrensCriteria:
	@classmethod
	def total_childrens(self):
		return _count(ch for ch in _newBorn)