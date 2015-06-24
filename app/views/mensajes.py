#-*- coding: utf-8 -*-
from __future__ import absolute_import
from ..tools import (route, BaseHandler)
from tornado.gen import (coroutine,)
from tornado.web import (authenticated, asynchronous)
from pony.orm import (db_session, select, desc)
from ..entities import (Mensaje, Agenda)
from ..criterias import (messagesCrt, agendaCrt, personsCrt)
from json import dumps, loads

from urllib import urlencode
from tornado.httpclient import AsyncHTTPClient

AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')

@route('/mensajes/gestion')
class MensajesGestion(BaseHandler):
	@authenticated
	@coroutine
	@asynchronous
	@db_session
	def get(self):
		mensajes = select(msg for msg in Mensaje if msg.tipo!=5).order_by(lambda msg: (msg.tipo, msg.nro_control, desc(msg.creado)))
		self.render('mensajes/gestion.html', mensajes=mensajes)

@route('/mensajes/adicionar_msj')
class AdicionarMsj(BaseHandler):
	@authenticated
	@coroutine
	@asynchronous
	def get(self):
		self.render('mensajes/adicionar_msj.html')
	@coroutine
	@asynchronous
	def post(self):
		self.set_header('Content-type', 'application/json')
		form = self.form2Dict()
		form.audio = self.rename_audio(form.tipo, form.nro_control)
		params = dict(
			status = messagesCrt.save(form=form, id_user=self.current_user.id),
			audio = form.audio
		)
		self.write(dumps(params))
		self.finish()
	def rename_audio(self, numb_status, numb_control, ext='mp3'):
		status = ['prenatal','postnatal','prom_prenatal','prom_postnatal','extraordinario']
		return '{}_{:02}.{}'.format(status[int(numb_status)-1], int(numb_control), ext)

@route('/mensajes/modificar_msj')
class ModificarMsj(BaseHandler):
	@authenticated
	@asynchronous
	@db_session
	def get(self):
		msg = Mensaje.get(**self.form2Dict())
		self.render('mensajes/modificar.html',msg=msg)
	@asynchronous
	def post(self):
		self.set_header('Content-type','application/json')
		flag = messagesCrt.update(id_user=self.current_user.id, **self.form2Dict())
		self.write(dumps(flag))
		self.finish()

@route('/mensajes/eliminar_msj')
class EliminarMsj(BaseHandler):
	@asynchronous
	def post(self):
		self.set_header('Content-type','application/json')
		flag = messagesCrt.delete(id_user=self.current_user.id, **self.form2Dict())
		self.write(dumps(flag))
		self.finish()

@route('/mensajes/sendsms')
class SendSMS(BaseHandler):
	@authenticated
	@coroutine
	@asynchronous
	@db_session
	def get(self):
		persons = personsCrt.get_All()
		self.render('mensajes/sendsms.html', personas=persons)
	@asynchronous
	@coroutine
	@db_session
	def post(self):
		self.set_header('Content-type', 'application/json')
		form = self.form2Dict(); form.tipo = 5
		if form.has_key('id_per'):
			del form.id_per
		#print form
		self.msg = messagesCrt.save(form=form, id_user=self.current_user.id, default=False)
		if self.msg:
			self.personas = [id_per for id_per in self.get_arguments('id_per') if len(id_per)]
			self.sendsms2cedes()
		self.write(dumps(True));
		self.finish()
	def persons2Json(self):
		contact = lambda pr: dict(contacto=pr.contacto.__str__(), ctelf=pr.contacto.telf) if not pr.telf else dict()
		person = lambda pr: dict(id_per=pr.id_per, nombre=pr.__str__(), telf=(pr.telf or None), **contact(pr))
		return dumps([person(personsCrt.get_byId(id_per)) for id_per in self.personas])
	"""
	def parse_sms(self, msg, personas):
		#query = lambda id_per: personsCrt.get_byId(id_per=id_per)
		contact = lambda pr: dict(contacto=pr.contacto.__str__(), ctelf=pr.contacto.telf) if not pr.telf else dict()
		person = lambda pr: dict(id_per=pr.id_per, nombre=pr.__str__(), telf=(pr.telf or None), **contact(pr))
		tmp = dumps([person(pr) for pr in personas])
		self.sendsms2cedes(msg, tmp)
	"""
	def sendsms2cedes(self):
		def handler(response):
			if loads(response.body):
				for id_per in self.personas:
					agendaCrt.save(persona=id_per, mensaje=self.msg.id_msj)
			else:
				messagesCrt.delete(id_msj=self.msg.id_msj, id_user=self.current_user.id)
		link = '190.129.142.26:8000/sendsms'
		data = urlencode(dict(msg=self.msg.tenor, personas=self.persons2Json()))
		cedes = AsyncHTTPClient()
		cedes.fetch(request=link, method='POST', body=data, expect_100_continue=True, request_timeout=120.0, callback=handler)

@route('/mensajes/agendas')
class Agendas(BaseHandler):
	@authenticated
	@asynchronous
	@db_session
	def get(self):
		agendas = select(ag for ag in Agenda).order_by(lambda ag: (ag.mensaje.usuario, ag.creado))
		self.render('mensajes/agendas.html', agendas=agendas)

@route('/api/getagenda')
class GetAgenda(BaseHandler):
	@asynchronous
	@coroutine
	@db_session
	def get(self):
		self.set_header('Content-type', 'application/json')
		apikey = self.application.settings['cookie_secret']
		try:
			query = self.form2Dict().apikey.encode('utf-8')
			if query == apikey:
				#agendas = [self.parse_agenda(ag) for ag in Agenda.select(lambda ag: ag.enviado==False)]
				self.write(self.parse_agenda())
			else:
				self.write('Error')
		except Exception, e:
			print e
			self.write('Error')
		self.finish()
	def parse_agenda(self):
		contact = lambda pr: dict(contacto=pr.contacto.__str__(), ctelf=pr.contacto.telf) if not pr.telf else dict()
		person = lambda pr: dict(nombre=pr.__str__(), telf=(pr.telf or None), **contact(pr))
		todict = lambda agenda: dict(
				id_agd = agenda.id_agd,
				fecha_msj = agenda.fecha_msj.isoformat(),
				fecha_con = agenda.fecha_con.isoformat(),
				tenor = agenda.mensaje.tenor,
				audio = agenda.mensaje.audio,
				**person(agenda.persona)
			)
		return dumps([todict(ag) for ag in Agenda.select(lambda ag: ag.enviado==False)])