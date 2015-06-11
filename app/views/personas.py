#-*- coding: utf-8 -*-
from __future__ import absolute_import
from ..tools import (route, BaseHandler, to_ddmmyy)
from tornado.web import (authenticated, asynchronous)
from pony.orm import (db_session, select)
from ..entities import (Tipo, Persona)
from ..criterias import personsCrt
from json import (dumps,)

@route('/personas/gestion')
class Gestion_Personas(BaseHandler):
	@authenticated
	@asynchronous
	@db_session
	def get(self):
		personas = select(pr for pr in Persona if not pr.usuario).order_by(lambda pr: (pr.nombres, pr.apellidos))
		self.render('personas/gestion.html', personas=personas, to_ddmmyy=to_ddmmyy)

@route('/personas/modificar')
class Modificar_Persona(BaseHandler):
	@authenticated
	@asynchronous
	@db_session
	def get(self):
		pr = Persona.get(**self.form2Dict())
		self.render('personas/modificar.html', pr=pr)
	@asynchronous
	def post(self):
		self.set_header('Content-type', 'application/json')
		self.write(dumps(personsCrt.update(**self.form2Dict())))
		self.finish()

@route('/personas/v_telf')
class V_Telf(BaseHandler):
	@asynchronous
	def post(self):
		self.set_header('Content-type', 'application/json')
		self.write(dumps(personsCrt.v_telf(**self.form2Dict())))
		self.finish()

@route('/personas/v_userstelf')
class V_UsersTelf(BaseHandler):
	@asynchronous
	@db_session
	def post(self):
		self.set_header('Content-type', 'application/json')
		pr = Persona.get(**self.form2Dict())
		self.write(dumps(None if(pr and pr.usuario) else True if pr else False))
		self.finish()

@route('/personas/v_pregnantstelf')
class V_PregnantsTelf(BaseHandler):
	@asynchronous
	@db_session
	def post(self):
		self.set_header('Content-type', 'application/json')
		pr = Persona.get(**self.form2Dict())
		o_response = {
			'status':True if(pr and pr.sexo=='f' and not find_pregnant(pr)) else None if pr else False,
			'p_data': pr.__str__() if pr else None
		}
		#self.write(dumps(True if(pr and pr.sexo=='f' and not find_pregnant(pr)) else None if pr else False))
		self.write(dumps(o_response))
		self.finish()

@route('/personas/getbycellphone')
class GetbyCellphone(BaseHandler):
	@asynchronous
	def post(self):
		self.set_header('Content-type', 'application/json')
		with db_session:
			pr = Persona.get(**self.form2Dict())
			if pr:
				tmp = dict(persona=pr.__str__(), id_per=pr.id_per, sexo=pr.sexo, nombres=pr.nombres, apellidos=pr.apellidos)
		self.write(dumps(tmp))
		self.finish()

@route('/personas/v_ci')
class V_CI(BaseHandler):
	@asynchronous
	def post(self):
		self.set_header('Content-type', 'application/json')
		self.write(dumps(personsCrt.v_ci(**self.form2Dict())))
		self.finish()

def find_pregnant(pregnant):
	tp = Tipo.get(id_tip=1)
	for tipo in pregnant.tipos:
		if tipo==tp:
			return True
	else:
		return False