#-*- coding: utf-8 -*-
from __future__ import absolute_import
from tornado.web import (authenticated, asynchronous)
from ..tools import (route, BaseHandler)
from pony.orm import db_session
from ..criterias import usersCrt
from json import (dumps,)

@route('/usuarios/gestion')
class Gestion_Usuarios(BaseHandler):
	@authenticated
	@asynchronous
	@db_session
	def get(self):
		usuarios = usersCrt.get_all()
		self.render('usuarios/gestion.html', usuarios=usuarios)

@route('/usuarios/nuevo_usuario')
class Nuevo_Usuario(BaseHandler):
	@authenticated
	@asynchronous
	def get(self):
		self.render('usuarios/nuevo_usuario.html')
	@asynchronous
	def post(self):
		self.set_header('Content-type', 'application/json')
		flag = usersCrt.save(self.form2Dict())
		self.write(dumps(flag))
		self.finish()

@route('/usuarios/modificar_usuario')
class Modificar_Usuario(BaseHandler):
	@authenticated
	@asynchronous
	@db_session
	def get(self):
		us = usersCrt.get(**self.form2Dict())
		self.render('usuarios/modificar_usuario.html', us=us)
	@asynchronous
	def post(self):
		self.set_header('Content-type', 'application/json')
		flag = usersCrt.update(self.form2Dict())
		self.write(dumps(flag))
		self.finish()

@route('/usuarios/eliminar_usuario')
class Eliminar_Usuario(BaseHandler):
	@asynchronous
	def post(self):
		if self.current_user.rol == u'Administrador':
			self.set_header('Content-type', 'application/json')
			self.write(dumps(usersCrt.delete(**self.form2Dict())))
			self.finish()

@route('/usuarios/v_login')
class V_Login(BaseHandler):
	@asynchronous
	def post(self):
		if self.current_user.rol == u'Administrador':
			self.set_header('Content-type', 'application/json')
			self.write(dumps(usersCrt.v_login(**self.form2Dict())))
			self.finish()

@route('/usuarios/v_ci')
class V_CI(BaseHandler):
	@asynchronous
	def post(self):
		if self.current_user.rol == u'Administrador':
			self.set_header('Content-type', 'application/json')
			self.write(dumps(usersCrt.v_ci(**self.form2Dict())))
			self.finish()

@route('/usuarios/profile')
class User_Profile(BaseHandler):
	@authenticated
	@asynchronous
	def get(self):
		self.render('usuarios/profile.html')

"""
@route('/usuarios/test_json')
class Test_Json(BaseHandler):
	def post(self):
		self.set_header('Content-type', 'application/json')
		with db_session:
			us = Usuario.get(**self.form2Dict())
			us = us.to_json() if us else None
		self.write(us)
"""