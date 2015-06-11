#-*- coding: utf:8 -*-
from __future__ import absolute_import
from ..tools import (utcDateTime as _utc)
from pony.orm import (db_session as _db_session, commit as _commit)
from ..entities import (Agenda as _Agenda)
from datetime import timedelta as _td

class AgendasCriteria:
	@classmethod
	def save(self, persona, mensaje, fecha_con=None, days=7):
		try:
			with _db_session:
				if fecha_con is None:
					now = _utc().now().date().isoformat()
					ag = _Agenda(persona=persona, mensaje=mensaje, fecha_msj=now, fecha_con=now, enviado=True)
				else:
					fecha_msj = (fecha_con - _td(days=days)).isoformat()
					fecha_con = fecha_con.isoformat()
					ag = _Agenda(persona=persona, mensaje=mensaje, fecha_msj=fecha_msj, fecha_con=fecha_con)
				_commit()
		except Exception, e:
			raise e
	@classmethod
	def delete_agendas(self, obj):
		utc = _utc()
		check_date = lambda dt: True if dt>=utc.now().date() else False
		with _db_session:
			for ags in obj.agendas:
				if not ags.enviado and check_date(ags.fecha_msj):
					ags.delete()
			_commit()