#-*- coding: utf-8 -*-
from __future__ import absolute_import
from tornado.web import authenticated
from ..tools import (route, BaseHandler)
from pony.orm import (db_session,)
from ..entities import Usuario
from ..criterias import (pregnantCrt, pregnant_status, childrensCrt, controlsCrt, usersCrt)
from json import dumps

@route('/')
class Index(BaseHandler):
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
	def get(self):
		self.render('main/login.html')
	@db_session
	def post(self):
		self.set_header('Content-type', 'application/json')
		form = self.form2Dict()
		if len(form.login) and len(form.passwd):
			us = usersCrt.granted_access(self.form2Dict())
			if us:
				self.set_secure_cookie('user', us.to_json(), expires_days=1)
			self.write(dumps(True if us else False))
		else:
			self.write(dumps(False))
		
@route('/logout')
class Logout(BaseHandler):
	def get(self):
		self.clear_all_cookies()
		self.redirect('/')