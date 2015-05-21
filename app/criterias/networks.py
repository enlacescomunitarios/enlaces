#-*- coding: utf-8 -*-
from pony.orm import (db_session as _db_session, commit as _commit, select as _select)
from ..entities import (Red_Salud as _Red_Salud, Municipio as _Municipio)

class NetworksCtriteria:
	@classmethod
	def get_All(self):
		return _select(nt for nt in _Red_Salud)
	@classmethod
	def save(self, form):
		try:
			with _db_session:
				red = _Red_Salud(nombre=form.nombre)
				#municipios = [dict(dpto=dpto, nombre=nombre, red_salud=red) for dpto, nombre in zip(self.get_arguments('dpto'),self.get_arguments('nombre')[1:])]
				red.municipios += [_Municipio(red_salud=red, **mn) for mn in form.municipios]
				_commit()
			return True
		except Exception, e:
			#raise e
			return False
	@classmethod
	def update(self, id_red, nombre):
		try:
			with _db_session:
				red = _Red_Salud.get(id_red=id_red)
				red.set(nombre=nombre, activo=True)
				_commit()
			return True
		except Exception, e:
			#raise e
			return False