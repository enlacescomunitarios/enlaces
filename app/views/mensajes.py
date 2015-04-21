#-*- coding: utf-8 -*-
from __future__ import absolute_import
from ..tools import (route, BaseHandler)
from pony.orm import (db_session, select)
from ..entities import (Mensaje,)
from ..criterias import messagesCrt
from json import dumps

@route('/mensajes/gestion')
class MensajesGestion(BaseHandler):
	@db_session
	def get(self):
		mensajes = select(msg for msg in Mensaje).order_by(lambda msg: (msg.tipo, msg.nro_control, msg.creado))
		self.render('mensajes/gestion.html', mensajes=mensajes)

@route('/mensajes/adicionar_msj')
class AdicionarMsj(BaseHandler):
	def get(self):
		self.render('mensajes/adicionar_msj.html')
	def post(self):
		self.set_header('Content-type', 'application/json')
		flag = messagesCrt.save(self.form2Dict())
		self.write(dumps(flag))

@route('/mensajes/modificar_msj')
class ModificarMsj(BaseHandler):
	@db_session
	def get(self):
		msg = Mensaje.get(**self.form2Dict())
		self.render('mensajes/modificar.html',msg=msg)
	def post(self):
		self.set_header('Content-type','application/json')
		flag = messagesCrt.update(**self.form2Dict())
		self.write(dumps(flag))

@route('/mensajes/eliminar_msj')
class EliminarMsj(BaseHandler):
	def post(self):
		self.set_header('Content-type','application/json')
		flag = messagesCrt.delete(**self.form2Dict())
		self.write(dumps(flag))