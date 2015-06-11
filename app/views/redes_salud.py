#-*- coding: utf-8 -*-
from __future__ import absolute_import
from tornado.web import (authenticated, asynchronous)
from ..tools import (route, BaseHandler, cdict)
from pony.orm import (db_session, commit)
from ..entities import (Red_Salud,)
from ..criterias import networksCrt
from json import dumps

@route(r'/redes_salud/gestion')
class Gestion_RedSalud(BaseHandler):
	@authenticated
	@asynchronous
	@db_session
	def get(self):
		redes = (rd for rd in Red_Salud.select())
		self.render('redes_salud/gestion.html', redes=redes, dumps=dumps)

@route(r'/redes_salud/nueva_red')
class Nueva_Red(BaseHandler):
	@authenticated
	@asynchronous
	def get(self):
		self.render('redes_salud/nueva_red.html')
	@asynchronous
	def post(self):
		self.set_header('Content-type', 'application/json')
		names = self.get_arguments('nombre')
		dptos = self.get_arguments('dpto')
		f_mups = lambda: dict(municipios=[dict(dpto=dpto, nombre=nombre) for dpto,nombre in zip(dptos, names[1:])])
		form = cdict(nombre=names[0], **f_mups())
		self.write(dumps(networksCrt.save(form)))
		self.finish()

@route(r'/redes_salud/modificar_red')
class Modificar_Red(BaseHandler):
	@authenticated
	@asynchronous
	@db_session
	def get(self):
		red = Red_Salud.get(**self.form2Dict())
		self.render('redes_salud/modificar_red.html', red=red)
	@asynchronous
	def post(self):
		self.set_header('Content-type', 'application/json')
		self.write(dumps(networksCrt.update(**self.form2Dict())))
		self.finish()

@route('/redes_salud/eliminar_red')
class Eliminar_Red(BaseHandler):
	@authenticated
	@asynchronous
	def post(self):
		if self.current_user.rol == u'Administrador':
			self.set_header("Content-type", "application/json")
			with db_session:
				red = Red_Salud.get(**self.form2Dict())
				if red:
					red.set(activo=False)
					commit()
			self.write(dumps(red.activo))
			self.finish()

@route('/redes_salud/disponibles')
class Redes_Disponibles(BaseHandler):
	@asynchronous
	def post(self):
		if self.current_user.rol == u'Administrador':
			self.set_header('Content-type', 'application/json')
			f_redes = lambda: [dict(id_red=rd.id_red, nombre=rd.nombre, municipios=f_municipios(rd), centros=f_centros(rd)) for rd in Red_Salud.select() if rd.activo]
			f_municipios = lambda red: [dict(id_mup=mp.id_mup, nombre=mp.nombre) for mp in red.municipios if mp.activo]
			f_centros = lambda red: [dict(id_cen=cn.id_cen, nombre=cn.nombre) for mp in red.municipios for com in mp.comunidades for cn in com.centros_salud if cn.activo]
			with db_session:
				redes = f_redes()
			self.write(dumps(redes))
			self.finish()

@route('/redes_salud/geografia')
class Redes_Geografia(BaseHandler):
	@asynchronous
	def post(self):
		self.set_header('Content-type', 'application/json')
		f_redes = lambda: [dict(id_red=rd.id_red, nombre=rd.nombre, municipios=f_municipios(rd)) for rd in Red_Salud.select(lambda rd: rd.activo)]
		f_municipios = lambda red: [dict(id_mup=mp.id_mup, nombre=mp.nombre, comunidades=f_comunidades(mp)) for mp in red.municipios if mp.activo]
		f_comunidades = lambda municipio: [dict(id_com=cm.id_com, nombre=cm.nombre) for cm in municipio.comunidades if cm.activo]
		with db_session:
			redes = f_redes()
		self.write(dumps(redes))
		self.finish()