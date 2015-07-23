#-*- coding: utf-8 -*-
from __future__ import absolute_import
from tornado.web import (authenticated, asynchronous)
from tornado.gen import coroutine
from ..tools import (route, BaseHandler)
from pony.orm import (db_session, commit)
from ..entities import (Etnia,)
from ..criterias import (ethnicCrt,)
from json import dumps

@route('/etnias/gestion')
class Gestion_Etnias(BaseHandler):
	@authenticated
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		etnias = (et for et in Etnia.select())
		self.render('etnias/gestion.html', etnias=etnias, dumps=dumps)

@route('/etnias/nueva_etnia')
class Nueva_Etnia(BaseHandler):
	@authenticated
	@asynchronous
	@coroutine
	def get(self):
		self.render('etnias/nueva_etnia.html')
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		status = ethnicCrt.save(**self.form2Dict())
		self.finish(dumps(status))

@route('/etnias/modificar_etnia')
class Modificar_Etnia(BaseHandler):
	@authenticated
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		et = Etnia.get(**self.form2Dict())
		self.render('etnias/modificar_etnia.html', et=et)
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		#print self.form2Dict()
		status = ethnicCrt.update(**self.form2Dict())
		self.finish(dumps(status))

@route('/etnias/eliminar_etnia')
class Eliminar_Etnia(BaseHandler):
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		with db_session:
			et = Etnia.get(**self.form2Dict())
			if et:
				et.set(activo=False)
				commit()
		self.finish(dumps(et.activo))

@route('/etnias/disponibles')
class Etnias_Disponibles(BaseHandler):
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		with db_session:
			etnias = dumps([dict(id_etn=et.id_etn,nombre=et.nombre) for et in Etnia.select(lambda et: et.activo)])
		self.finish(etnias)