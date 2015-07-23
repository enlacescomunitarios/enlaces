#-*- coding: utf-8 -*-
from __future__ import absolute_import
from tornado.web import (authenticated, asynchronous)
from tornado.gen import coroutine
from ..tools import (route, BaseHandler, to_ddmmyy)
from pony.orm import (db_session, select)
from ..entities import (Tipo, Persona)
from ..criterias import personsCrt
from json import (dumps,)

@route('/personas/gestion')
class Gestion_Personas(BaseHandler):
	@authenticated
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		personas = select(pr for pr in Persona if not pr.usuario).order_by(lambda pr: (pr.nombres, pr.apellidos))
		self.render('personas/gestion.html', personas=personas, to_ddmmyy=to_ddmmyy)

@route('/personas/modificar')
class Modificar_Persona(BaseHandler):
	@authenticated
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		pr = Persona.get(**self.form2Dict())
		self.render('personas/modificar.html', pr=pr)
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		self.finish(dumps(personsCrt.update(**self.form2Dict())))

@route('/personas/v_telf')
class V_Telf(BaseHandler):
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		self.finish(dumps(personsCrt.v_telf(**self.form2Dict())))

@route('/personas/v_userstelf')
class V_UsersTelf(BaseHandler):
	@db_session
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		pr = Persona.get(**self.form2Dict())
		self.finish(dumps(None if(pr and pr.usuario) else True if pr else False))

@route('/personas/v_pregnantstelf')
class V_PregnantsTelf(BaseHandler):
	@db_session
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		pr = Persona.get(**self.form2Dict())
		o_response = {
			'status':True if(pr and pr.sexo=='f' and not find_pregnant(pr)) else None if pr else False,
			'p_data': pr.__str__() if pr else None
		}
		#self.finish(dumps(True if(pr and pr.sexo=='f' and not find_pregnant(pr)) else None if pr else False))
		self.finish(dumps(o_response))

@route('/personas/getbycellphone')
class GetbyCellphone(BaseHandler):
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		with db_session:
			pr = Persona.get(**self.form2Dict())
			if pr:
				tmp = dict(persona=pr.__str__(), id_per=pr.id_per, sexo=pr.sexo, nombres=pr.nombres, apellidos=pr.apellidos)
		self.finish(dumps(tmp))

@route('/personas/v_ci')
class V_CI(BaseHandler):
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		self.finish(dumps(personsCrt.v_ci(**self.form2Dict())))

def find_pregnant(pregnant):
	tp = Tipo.get(id_tip=1)
	for tipo in pregnant.tipos:
		if tipo==tp:
			return True
	else:
		return False