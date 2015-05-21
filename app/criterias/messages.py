#-*- coding: utf-8 -*-
from __future__ import absolute_import
from pony.orm import (db_session as _db_session, commit as _commit, select as _select)
from ..entities import (Mensaje as _Mensaje,)

class MessagesCriteria:
	@classmethod
	def check(self, tipo=None, nro_control=None, titulo=None, id_msj=None):
		with _db_session:
			if nro_control:
				return _select(msg for msg in _Mensaje if int(nro_control)==msg.nro_control and int(tipo)==msg.tipo and msg.activo==True).exists()
			else:
				if id_msj:
					tmp = _Mensaje.select(lambda msg: id_msj!=msg.id_msj and msg.titulo==titulo and msg.activo==True).count()
					return False if tmp==0 else True
				else:
					return _select(msg for msg in _Mensaje if titulo==msg.titulo and int(tipo)==msg.tipo and msg.activo==True).exists()
	@classmethod
	def save(self, form):
		flag = self.check(nro_control=form.nro_control,tipo=form.tipo) if hasattr(form,'nro_control') else self.check(titulo=form.titulo,tipo=form.tipo)
		#print flag
		if not flag:
			with _db_session:
				msg = _Mensaje(**form); _commit()
		return not flag
	@classmethod
	def update(self, id_msj, tenor, titulo=None):
		flag = True
		with _db_session:
			msg = _Mensaje.get(id_msj=id_msj)
			if titulo is not None:
				#print self.check(id_msj=msg.id_msj,titulo=titulo)
				if titulo!=msg.titulo and not self.check(titulo=titulo,tipo=4):
					msg.set(titulo=titulo, tenor=tenor, activo=True); _commit()
				elif titulo==msg.titulo and not self.check(id_msj=msg.id_msj,titulo=titulo):
					msg.set(tenor=tenor, activo=True); _commit()
				else:
					flag = False
			else:
				msg.set(tenor=tenor, activo=True); _commit()
		return flag
	@classmethod
	def delete(self, id_msj):
		with _db_session:
			msg = _Mensaje.get(id_msj=id_msj)
			msg.set(activo=False); _commit()
		return msg.activo