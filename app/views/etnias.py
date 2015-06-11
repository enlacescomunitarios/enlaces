#-*- coding: utf-8 -*-
from __future__ import absolute_import
from ..tools import (route, BaseHandler)
from tornado.web import (authenticated, asynchronous)
from pony.orm import (db_session, commit)
from ..entities import (Etnia,)
from ..criterias import (ethnicCrt,)
from json import dumps

@route('/etnias/gestion')
class Gestion_Etnias(BaseHandler):
	@authenticated
	@asynchronous
	@db_session
	def get(self):
		etnias = (et for et in Etnia.select())
		self.render('etnias/gestion.html', etnias=etnias, dumps=dumps)

@route('/etnias/nueva_etnia')
class Nueva_Etnia(BaseHandler):
	@authenticated
	@asynchronous
	def get(self):
		self.render('etnias/nueva_etnia.html')
	@asynchronous
	def post(self):
		self.set_header('Content-type', 'application/json')
		status = ethnicCrt.save(**self.form2Dict())
		self.write(dumps(status))
		self.finish()

@route('/etnias/modificar_etnia')
class Modificar_Etnia(BaseHandler):
	@authenticated
	@asynchronous
	@db_session
	def get(self):
		et = Etnia.get(**self.form2Dict())
		self.render('etnias/modificar_etnia.html', et=et)
	@asynchronous
	def post(self):
		self.set_header('Content-type', 'application/json')
		#print self.form2Dict()
		status = ethnicCrt.update(**self.form2Dict())
		self.write(dumps(status))
		self.finish()

@route('/etnias/eliminar_etnia')
class Eliminar_Etnia(BaseHandler):
	@asynchronous
	def post(self):
		self.set_header('Content-type', 'application/json')
		with db_session:
			et = Etnia.get(**self.form2Dict())
			if et:
				et.set(activo=False)
				commit()
		self.write(dumps(et.activo))
		self.finish()

@route('/etnias/disponibles')
class Etnias_Disponibles(BaseHandler):
	@asynchronous
	def post(self):
		self.set_header('Content-type', 'application/json')
		with db_session:
			etnias = dumps([dict(id_etn=et.id_etn,nombre=et.nombre) for et in Etnia.select(lambda et: et.activo)])
		self.write(etnias)
		self.finish()