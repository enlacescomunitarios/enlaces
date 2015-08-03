#-*- coding: utf-8 -*-
from pony.orm import (select as _select, count as _count, db_session as _db_session, commit as _commit)
from ..entities import (Control as _Control)
from ..tools import utc as _utc

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
		check_date = lambda dt: True if dt>=_utc.now().date() else False
		with _db_session:
			for cnt in obj.controles:
				if not cnt.asistido and check_date(cnt.fecha_con):
					cnt.delete()
			_commit()