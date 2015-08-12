#-*- coding: utf-8 -*-
from tornado.web import (asynchronous,)
from tornado.gen import (coroutine,)
from ..tools import (route, BaseHandler)
from pony.orm import (db_session,)
from ..entities import (Mensaje, Agenda)
from ..criterias import (personsCrt,)

from json import dumps

@route('/api/getpersons')
class GetPersons(BaseHandler):
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		self.set_header('Content-type', 'application/json')
		int_key, form = self.application.settings['cookie_secret'], self.form2Dict()
		ext_key = form.apikey.encode('utf-8') if form.has_key('apikey') else None
		if int_key==ext_key:
			self.finish(dumps([pr.to_dict() for pr in personsCrt.get_api()]))
		else:
			self.finish('Error')

@route('/api/getmessages')
class GetMessages(BaseHandler):
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		self.set_header('Content-type', 'application/json')
		int_key, form = self.application.settings['cookie_secret'], self.form2Dict()
		ext_key = form.apikey.encode('utf-8') if form.has_key('apikey') else None
		if int_key==ext_key:
			self.finish(dumps([msg.to_dict() for msg in Mensaje.select(lambda msg: msg.tipo>=1 and msg.tipo<=4)]))
		else:
			self.finish('Error')

@route('/api/getagenda')
class GetAgenda(BaseHandler):
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		self.set_header('Content-type', 'application/json')
		int_key, form = self.application.settings['cookie_secret'], self.form2Dict()
		ext_key = form.apikey.encode('utf-8') if form.has_key('apikey') else None
		x_real_ip = self.request.headers.get("X-Real-IP")
		remote_ip = self.request.remote_ip if not x_real_ip else x_real_ip
		print remote_ip
		if int_key == ext_key:
			self.finish(dumps([ag.to_dict() for ag in Agenda.select(lambda ag: not ag.enviado)]))
		else:
			self.finish('Error')