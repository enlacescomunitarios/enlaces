#-*- coding: utf-8 -*-
from tornado.gen import coroutine
from tornado.web import (authenticated, asynchronous)
from ..tools import (route, BaseHandler)
from pony.orm import db_session
from ..criterias import usersCrt
from json import (dumps,)

@route('/usuarios/gestion')
class Gestion_Usuarios(BaseHandler):
	@authenticated
	@asynchronous
	@coroutine
	@db_session
	def get(self):
		usuarios = usersCrt.get_all()
		self.render('usuarios/gestion.html', usuarios=usuarios)

@route('/usuarios/nuevo_usuario')
class Nuevo_Usuario(BaseHandler):
	@authenticated
	@asynchronous
	@coroutine
	def get(self):
		self.render('usuarios/nuevo_usuario.html')
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		flag = usersCrt.save(self.form2Dict())
		self.finish(dumps(flag))

@route('/usuarios/modificar_usuario')
class Modificar_Usuario(BaseHandler):
	@authenticated
	@asynchronous
	@coroutine
	@db_session
	def get(self):
		us = usersCrt.get(**self.form2Dict())
		self.render('usuarios/modificar_usuario.html', us=us)
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		flag = usersCrt.update(self.form2Dict())
		self.finish(dumps(flag))

@route('/usuarios/eliminar_usuario')
class Eliminar_Usuario(BaseHandler):
	@asynchronous
	@coroutine
	def post(self):
		if self.current_user.rol == u'Administrador':
			self.set_header('Content-type', 'application/json')
			self.finish(dumps(usersCrt.delete(**self.form2Dict())))

@route('/usuarios/v_login')
class V_Login(BaseHandler):
	@asynchronous
	@coroutine
	def post(self):
		if self.current_user.rol == u'Administrador':
			self.set_header('Content-type', 'application/json')
			self.finish(dumps(usersCrt.v_login(**self.form2Dict())))

@route('/usuarios/v_ci')
class V_CI(BaseHandler):
	@asynchronous
	@coroutine
	def post(self):
		if self.current_user.rol == u'Administrador':
			self.set_header('Content-type', 'application/json')
			self.finish(dumps(usersCrt.v_ci(**self.form2Dict())))

@route('/usuarios/profile')
class User_Profile(BaseHandler):
	@authenticated
	@asynchronous
	@coroutine
	@db_session
	def get(self):
		userprofl = usersCrt.get(persona=self.current_user.id)
		self.render('usuarios/profile.html', userprofl=userprofl)
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		form = self.form2Dict()
		success = usersCrt.update(form)
		if success:
			self.clear_all_cookies()
			with db_session:
				us = usersCrt.get(login=form.login)
				self.set_secure_cookie('user', us.to_json(), expires_days=None)
		self.finish(dumps(success))

"""
@route('/usuarios/test_json')
class Test_Json(BaseHandler):
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		with db_session:
			us = Usuario.get(**self.form2Dict())
			us = us.to_json() if us else None
		self.finish(us)
"""