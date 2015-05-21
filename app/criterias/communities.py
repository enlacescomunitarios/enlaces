#-*- coding: utf-8 -*-
from pony.orm import (db_session as _db_session, commit as _commit, select as _select)
from ..entities import (Municipio as _Municipio, Comunidad as _Comunidad, Centro_Salud as _Centro_Salud)

class CommunitiesCriteria:
	@classmethod
	def get_All(self):
		return _select(cm for cm in _Comunidad).order_by(lambda cm: (cm.municipio, cm.nombre))
	@classmethod
	def save(self, id_mup, community, hospitals):
		try:
			with _db_session:
				com = _Comunidad(municipio=_Municipio.get(id_mup=id_mup), **community)
				for hp in hospitals:
					hospital = _Centro_Salud(ubicado=com, **hp)
					hospital.comunidades += [com]
				_commit()
			return True
		except Exception, e:
			#raise e
			return False
	@classmethod
	def update(self, id_com, nombre, telf):
		try:
			with _db_session:
				com = _Comunidad.get(id_com=id_com)
				com.set(nombre=nombre, telf=telf, activo=True)
				_commit()
			return True
		except Exception, e:
			#raise e
			return False
	@classmethod
	def delete(self, id_com):
		try:
			with _db_session:
				com = _Comunidad.get(id_com=id_com)
				com.set(activo=False)
				_commit()
			return False
		except Exception, e:
			#raise e
			return True