#-*- coding: utf-8 -*-
from __future__ import absolute_import
from ..tools import (route, BaseHandler)
from pony.orm import (db_session,)
from ..entities import (Tipo,)
from ..criterias import typeCrt
from json import dumps

@route('/tipos/gestion')
class Gestion_Tipos(BaseHandler):
	@db_session
	def get(self):
		tipos = (tp for tp in Tipo.select())
		self.render('tipos/gestion.html', tipos=tipos, dumps=dumps)

@route('/tipos/nuevo_tipo')
class Nuevo_Tipo(BaseHandler):
	def get(self):
		self.render('tipos/nuevo_tipo.html')
	def post(self):
		self.set_header('Content-type', 'application/json')
		status = typeCrt.save(**self.form2Dict())
		self.write(dumps(status))

@route('/tipos/modificar_tipo')
class Modificar_Tipo(BaseHandler):
	@db_session
	def get(self):
		tp = Tipo.get(**self.form2Dict())
		self.render('tipos/modificar_tipo.html', tp=tp)
	def post(self):
		self.set_header('Content-type', 'application/json')
		status = typeCrt.update(**self.form2Dict())
		self.write(dumps(status))

@route('/tipos/disponibles')
class Tipos_Disponible(BaseHandler):
	def post(self):
		self.set_header('Content-type', 'application/json')
		with db_session:
			tipos = [dict(id_tip=tp.id_tip,nombre=tp.nombre) for tp in Tipo.select() if tp.activo]
		self.write(dumps(tipos))