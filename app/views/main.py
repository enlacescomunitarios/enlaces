#-*- coding: utf-8 -*-
from __future__ import absolute_import
from tornado.gen import (coroutine,)
from tornado.web import (authenticated, asynchronous)
from ..tools import (route, BaseHandler)
from pony.orm import (db_session,)
#from ..entities import Usuario
from ..criterias import (pregnantCrt, pregnant_status, childrensCrt, controlsCrt, usersCrt)
from json import dumps

@route('/')
class Index(BaseHandler):
	@asynchronous
	@coroutine
	@authenticated
	@db_session
	def get(self):
		params = dict(
			embarazadas = pregnantCrt.get_all(), emb_status = pregnant_status, mujeres = pregnantCrt.total_womens(),
			embarazos = pregnantCrt.total_pregnants(), bebes = childrensCrt.total_childrens(), controles = controlsCrt.total_checked(),
		)
		self.render('main/index.html', **params)

@route('/login')
class Login(BaseHandler):
	@asynchronous
	def get(self):
		self.render('main/login.html')
	@asynchronous
	@db_session
	def post(self):
		self.set_header('Content-type', 'application/json')
		form = self.form2Dict()
		if len(form.login) and len(form.passwd):
			us = usersCrt.granted_access(self.form2Dict())
			if us:
				self.set_secure_cookie('user', us.to_json(), expires_days=None)#without persistence
			self.write(dumps(True if us else False))
		else:
			self.write(dumps(False))
		self.finish()
		
@route('/logout')
class Logout(BaseHandler):
	def get(self):
		self.clear_all_cookies()
		self.redirect('/')