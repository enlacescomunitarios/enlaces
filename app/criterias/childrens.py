#-*- coding: utf-8 -*-
from __future__ import absolute_import
from ..tools import (getLocals as _getLocals, to_yymmdd as _to_yymmdd)
from pony.orm import (db_session as _db_session, commit as _commit, select as _select, count as _count)
from ..entities import (Recien_Nacido as _newBorn, Defuncion as _Death)
from .controls import ControlsCriteria as _controlsCrt

class ChildrensCriteria:
	@classmethod
	def total_childrens(self):
		return _count(ch for ch in _newBorn)
	@classmethod
	def update(self, id_rcn, nombres, apellidos, sexo, peso):
		try:
			with _db_session:
				child = _newBorn.get(id_rcn=id_rcn)
				child.set(nombres=nombres, apellidos=apellidos, sexo=sexo, peso=peso)
				_commit()
			return True
		except Exception, e:
			raise e
			return False
	@classmethod
	def death(self, id_rcn, fecha, f_notf, obs_notf, f_conf=None, obs_conf=None):
		deathForm = _getLocals(locals())
		deathForm.fecha, deathForm.f_notf = _to_yymmdd(fecha), _to_yymmdd(f_notf)
		try:
			with _db_session:
				child = _newBorn.get(id_rcn=id_rcn)
				del deathForm.id_rcn
				if f_conf is not None:
					deathForm.f_conf = _to_yymmdd(f_conf)
					_controlsCrt.delete_controls(child)
				death = _Death(recien_nacido=child, **deathForm)
				_commit()
			return True
		except Exception, e:
			raise e
			return False
	@classmethod
	def confirm_death(self, id_def, f_conf, obs_conf):
		try:
			with _db_session:
				death = _Death.get(id_def=id_def)
				death.set(f_conf=_to_yymmdd(f_conf), obs_conf=obs_conf)
				_controlsCrt.delete_controls(death.recien_nacido)
				_commit()
			return True
		except Exception, e:
			raise e
			return False
	@classmethod
	def delete_death(self, id_def):
		try:
			with _db_session:
				death = _Death.get(id_def=id_def)
				death.delete()
				_commit()
			return False
		except Exception, e:
			raise e
			return True