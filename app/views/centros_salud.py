#-*- coding: utf-8 -*-
from __future__ import absolute_import
from ..tools import (route, BaseHandler)
from tornado.web import (authenticated, asynchronous)
from pony.orm import (db_session, commit)
from ..entities import (Comunidad, Centro_Salud, Prestacion)
from json import dumps

@route('/centros_salud/gestion')
class Gestion_Centros(BaseHandler):
	@authenticated
	@asynchronous
	@db_session
	def get(self):
		com = Comunidad.get(**self.form2Dict())
		self.render('centros_salud/gestion.html', com=com, dumps=dumps)

@route('/centros_salud/nuevo_establecimiento')
class Nuevo_Establecimiento(BaseHandler):
	@authenticated
	@asynchronous
	@db_session
	def get(self):
		com = Comunidad.get(**self.form2Dict())
		self.render('centros_salud/nuevo_establecimiento.html', com=com, dumps=dumps)
	@asynchronous
	def post(self):
		with db_session:
			ubicado = Comunidad.get(id_com=self.get_arguments('id_com')[0])
			cs = Centro_Salud(tipo=self.get_argument('tipo'),nombre=self.get_argument('nombre'),ubicado=ubicado)
			cs.comunidades += [Comunidad.get(id_com=id_com) for id_com in self.get_arguments('id_com')[1:]]
			cs.comunidades += [ubicado]
			cs.prestaciones += [Prestacion.get(id_pst=id_pst) for id_pst in self.get_arguments('id_pst')]
			commit()
		self.redirect('/centros_salud/gestion?id_com={}'.format(ubicado.id_com))

@route('/centros_salud/modificar_establecimiento')
class Modificar_Establecimiento(BaseHandler):
	@authenticated
	@asynchronous
	@db_session
	def get(self):
		cen = Centro_Salud.get(**self.form2Dict())
		self.render('centros_salud/modificar_establecimiento.html', cen=cen, dumps=dumps)
	@asynchronous
	def post(self):
		with db_session:
			cen = Centro_Salud.get(id_cen=self.get_argument('id_cen'))
			cen.set(tipo=self.get_argument('tipo'), nombre=self.get_argument('nombre'), activo=True)
			if not cen.comunidades.is_empty():
				cen.comunidades.clear()
			cen.comunidades += [Comunidad.get(id_com=id_com) for id_com in self.get_arguments('id_com')]
			cen.comunidades += [cen.ubicado]
			if not cen.prestaciones.is_empty():
				cen.prestaciones.clear()
			cen.prestaciones += [Prestacion.get(id_pst=id_pst) for id_pst in self.get_arguments('id_pst')]
			commit()
		self.redirect('/centros_salud/gestion?id_com={}'.format(cen.ubicado.id_com))

@route('/centros_salud/eliminar_establecimiento')
class Eliminar_Establecimiento(BaseHandler):
	@asynchronous
	def post(self):
		self.set_header('Content-type', 'application/json')
		with db_session:
			cs = Centro_Salud.get(**self.form2Dict())
			if cs:
				cs.activo = False
				if not cs.comunidades.is_empty():
					cs.comunidades.clear()
				if not cs.prestaciones.is_empty():
					cs.prestaciones.clear()
				commit()
		self.write(dumps(cs.activo))
		self.finish()

@route('/centros_salud')
class Listar_Centros(BaseHandler):
	@authenticated
	@asynchronous
	@db_session
	def get(self):
		centros = (cs for cs in Centro_Salud.select().order_by(lambda cs:(cs.ubicado,)))
		self.render('centros_salud/establecimientos.html', centros=centros)