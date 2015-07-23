#-*- coding: utf-8 -*-
from __future__ import absolute_import
from tornado.web import asynchronous
from tornado.gen import coroutine
from ..tools import (route, BaseHandler)
from pony.orm import (db_session,)
from ..entities import (Municipio, Comunidad)
from ..criterias import communitiesCrt
from json import dumps

@route('/comunidades/gestion')
class Gestion_Comunidades(BaseHandler):
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		mup = Municipio.get(**self.form2Dict())
		self.render('comunidades/gestion.html', mup=mup, dumps=dumps)

@route('/comunidades/nueva_comunidad')
class Nueva_Comunidad(BaseHandler):
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		mup = Municipio.get(**self.form2Dict())
		self.render('comunidades/nueva_comunidad.html', mup=mup, dumps=dumps)
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		id_mup = self.get_argument('id_mup')
		o_com = dict(nombre=self.get_arguments('nombre')[0], telf=self.get_argument('telf'))
		centros = [dict(nombre=nombre,tipo=tipo) for nombre,tipo in zip(self.get_arguments('nombre')[1:],self.get_arguments('tipo'))]
		self.finish(dumps(communitiesCrt.save(id_mup, o_com, centros)))

@route('/comunidades/modificar_comunidad')
class Modificar_Comunidad(BaseHandler):
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		com = Comunidad.get(**self.form2Dict())
		self.render('comunidades/modificar_comunidad.html', com=com, dumps=dumps)
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		self.finish(dumps(communitiesCrt.update(**self.form2Dict())))

@route(r'/comunidades/elimininar_comunidad')
class Eliminar_Comunidad(BaseHandler):
	@asynchronous
	@coroutine
	def post(self):
		self.set_header("Content-type", "application/json")
		self.finish(dumps(communitiesCrt.delete(**self.form2Dict())))