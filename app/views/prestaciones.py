from __future__ import absolute_import
from ..tools import (route, BaseHandler)
from tornado.web import (authenticated, asynchronous)
from pony.orm import (db_session,)
from ..entities import (Prestacion,)
from ..criterias import capabilityCrt
from json import dumps, loads

@route('/prestaciones/gestion')
class Gestion_Prestaciones(BaseHandler):
	@authenticated
	@asynchronous
	@db_session
	def get(self):
		prestaciones = (pr for pr in Prestacion.select())
		self.render('prestaciones/gestion.html', prestaciones=prestaciones, dumps=dumps)

@route('/prestaciones/nueva_prestacion')
class Nueva_Prestacion(BaseHandler):
	@authenticated
	@asynchronous
	def get(self):
		self.render('prestaciones/nueva_prestacion.html')
	@asynchronous
	def post(self):
		self.set_header('Content-type', 'application/json')
		status = capabilityCrt.save(**self.form2Dict())
		self.write(dumps(status))
		self.finish()

@route('/prestaciones/modificar_prestacion')
class Modificar_prestacion(BaseHandler):
	@authenticated
	@asynchronous
	@db_session
	def get(self):
		pr = Prestacion.get(**self.form2Dict())
		self.render('prestaciones/modificar_prestacion.html', pr=pr)
	@asynchronous
	def post(self):
		self.set_header('Content-type', 'application/json')
		status = capabilityCrt.update(**self.form2Dict())
		self.write(dumps(status))
		self.finish()

@route('/prestaciones/eliminar_prestacion')
class Eliminar_Prestacion(BaseHandler):
	@asynchronous
	def post(self):
		self.set_header('Content-type', 'application/json')
		status = capabilityCrt.delete(**self.form2Dict())
		self.write(dumps(status))
		self.finish()

@route('/prestaciones/disponibles')
class Prestaciones_Disponibles(BaseHandler):
	@asynchronous
	@db_session
	def post(self):
		self.set_header('Content-type', 'application/json')
		ids = loads(self.get_argument('prestaciones'))
		disponibles = [dict(id_pst=pr.id_pst, nombre=pr.nombre) for pr in Prestacion.select() if pr.activo and pr.id_pst not in ids]
		self.write(dumps(disponibles))
		self.finish()