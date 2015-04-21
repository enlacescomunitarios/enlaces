#-*- coding: utf-8 -*-
from __future__ import absolute_import
from pony.orm import (db_session as _db_session, commit as _commit, select as _select, count as _count)
from ..entities import (Embarazo as _Embarazo, Control as _Control)
from ..tools import utcDateTime as _utcDateTime

class ControlsCriteria:
	@classmethod
	def total_checked(self):
		return _count(cn for cn in _Control if cn.asistido)
	@classmethod
	def getbyPregnancy(self, id_emb):
		return _select(ct for ct in _Control if ct.embarazo.id_emb==id_emb).order_by(lambda ct: (ct.nro_con, ct.fecha_con))
	@classmethod
	def getbyChild(self, id_rcn):
		return _select(ct for ct in _Control if ct.recien_nacido.id_rcn==id_rcn).order_by(lambda ct: (ct.nro_con, ct.fecha_con))
	@classmethod
	def delete_controls(self, obj):
		utc = _utcDateTime()
		check_date = lambda dt: True if dt>=utc.now().date() else False
		for cnt in obj.controles:
			if not cnt.asistido and check_date(cnt.fecha_con):
				cnt.delete()