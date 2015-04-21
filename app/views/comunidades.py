#-*- coding: utf-8 -*-
from __future__ import absolute_import
from ..tools import (route, BaseHandler)
from pony.orm import (db_session, commit)
from ..entities import (Municipio, Comunidad, Centro_Salud)
from ..criterias import communitiesCrt
from json import dumps

@route('/comunidades/gestion')
class Gestion_Comunidades(BaseHandler):
	@db_session
	def get(self):
		mup = Municipio.get(**self.form2Dict())
		self.render('comunidades/gestion.html', mup=mup, dumps=dumps)

@route('/comunidades/nueva_comunidad')
class Nueva_Comunidad(BaseHandler):
	@db_session
	def get(self):
		mup = Municipio.get(**self.form2Dict())
		self.render('comunidades/nueva_comunidad.html', mup=mup, dumps=dumps)
	def post(self):
		self.set_header('Content-type', 'application/json')
		id_mup = self.get_argument('id_mup')
		o_com = dict(nombre=self.get_arguments('nombre')[0], telf=self.get_argument('telf'))
		centros = [dict(nombre=nombre,tipo=tipo) for nombre,tipo in zip(self.get_arguments('nombre')[1:],self.get_arguments('tipo'))]
		self.write(dumps(communitiesCrt.save(id_mup, o_com, centros)))

@route('/comunidades/modificar_comunidad')
class Modificar_Comunidad(BaseHandler):
	@db_session
	def get(self):
		com = Comunidad.get(**self.form2Dict())
		self.render('comunidades/modificar_comunidad.html', com=com, dumps=dumps)
	def post(self):
		self.set_header('Content-type', 'application/json')
		self.write(dumps(communitiesCrt.update(**self.form2Dict())))

@route(r'/comunidades/elimininar_comunidad')
class Eliminar_Comunidad(BaseHandler):
	def post(self):
		self.set_header("Content-type", "application/json")
		self.write(dumps(communitiesCrt.delete(**self.form2Dict())))