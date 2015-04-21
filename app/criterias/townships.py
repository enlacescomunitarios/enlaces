#-*- coding:utf-8 -*-
from pony.orm import (db_session as _db_session, commit as _commit, select as _select)
from ..entities import (Red_Salud as _Red_Salud, Municipio as _Municipio, Comunidad as _Comunidad)

class TownshipsCriteria:
	@classmethod
	def get_All(self):
		return _select(tn for tn in _Comunidad)
	@classmethod
	def save(self, township, communities):
		try:
			with _db_session:
				township = _Municipio(**township)
				township.comunidades += [_Comunidad(municipio=township, **com) for com in communities]
				_commit()
			return True
		except Exception, e:
			#raise e
			return False
	@classmethod
	def update(self, id_mup, nombre, dpto):
		try:
			with _db_session:
				mup = _Municipio.get(id_mup=id_mup)
				mup.set(nombre=nombre, dpto=dpto, activo=True)
				_commit()
			return True
		except Exception, e:
			#raise e
			return False
	@classmethod
	def delete(self, id_mup):
		try:
			with _db_session:
				mup = _Municipio.get(id_mup=id_mup)
				mup.set(activo=False)
				_commit()
			return False
		except Exception, e:
			#raise e
			return True