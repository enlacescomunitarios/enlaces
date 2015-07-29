#-*- coding: utf-8 -*-
from __future__ import absolute_import
from tornado.web import (authenticated, asynchronous)
from tornado.gen import coroutine
from ..tools import (route, BaseHandler, utcDateTime, to_ddmmyy, cdict, ReportMaker)
from pony.orm import (db_session, select, desc)
from ..entities import (Mensaje, Agenda)
from ..criterias import (messagesCrt, agendaCrt, personsCrt)
from json import dumps, loads

from urllib import urlencode
from tornado.httpclient import (AsyncHTTPClient,)
from os import (path, sep)

AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')
utc = utcDateTime()

@route('/mensajes/gestion')
class MensajesGestion(BaseHandler):
	@authenticated
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		mensajes = select(msg for msg in Mensaje if msg.tipo!=5).order_by(lambda msg: (msg.tipo, msg.nro_control, desc(msg.creado)))
		self.render('mensajes/gestion.html', mensajes=mensajes)

@route('/mensajes/adicionar_msj')
class AdicionarMsj(BaseHandler):
	@authenticated
	@asynchronous
	@coroutine
	def get(self):
		self.render('mensajes/adicionar_msj.html')
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		form = self.form2Dict()
		form.audio = self.rename_audio(form.tipo, form.nro_control)
		params = dict(
			status = messagesCrt.save(form=form, id_user=self.current_user.id),
			audio = form.audio
		)
		self.finish(dumps(params))
	def rename_audio(self, numb_status, numb_control, ext='mp3'):
		status = ['prenatal','postnatal','prom_prenatal','prom_postnatal','extraordinario']
		return '{}_{:02}.{}'.format(status[int(numb_status)-1], int(numb_control), ext)

@route('/mensajes/modificar_msj')
class ModificarMsj(BaseHandler):
	@authenticated
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		msg = Mensaje.get(**self.form2Dict())
		self.render('mensajes/modificar.html',msg=msg)
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type','application/json')
		flag = messagesCrt.update(id_user=self.current_user.id, **self.form2Dict())
		self.finish(dumps(flag))

@route('/mensajes/eliminar_msj')
class EliminarMsj(BaseHandler):
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type','application/json')
		flag = messagesCrt.delete(id_user=self.current_user.id, **self.form2Dict())
		self.finish(dumps(flag))

@route('/mensajes/sendsms')
class SendSMS(BaseHandler):
	@authenticated
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		persons = personsCrt.get_All()
		self.render('mensajes/sendsms.html', personas=persons)
	@db_session
	@asynchronous
	@coroutine
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
		self.finish(dumps(True))
	def persons2Json(self):
		contact = lambda pr: dict(contacto=pr.contacto.__str__(), ctelf=pr.contacto.telf) if not pr.telf else dict()
		person = lambda pr: dict(id_per=pr.id_per, nombre=pr.__str__(), telf=(pr.telf or None), **contact(pr))
		return dumps([person(personsCrt.get_byId(id_per)) for id_per in self.personas])
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
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		agendas = select(ag for ag in Agenda).order_by(lambda ag: (ag.mensaje.usuario, ag.creado))
		self.render('mensajes/agendas.html', agendas=agendas)

@route('/api/getagenda')
class GetAgenda(BaseHandler):
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		self.set_header('Content-type', 'application/json')
		apikey = self.application.settings['cookie_secret']
		x_real_ip = self.request.headers.get("X-Real-IP")
		remote_ip = self.request.remote_ip if not x_real_ip else x_real_ip
		print remote_ip
		try:
			query = self.form2Dict().apikey.encode('utf-8')
			if query == apikey:
				self.finish(self.parse_agenda())
			else:
				self.finish('Error')
		except Exception, e:
			print e
			self.finish('Error')
		
	def parse_agenda(self):
		contact = lambda pr: dict(contacto=pr.contacto.__str__(), ctelf=pr.contacto.telf) if not pr.telf else dict()
		person = lambda pr: dict(nombre=pr.__str__(), telf=(pr.telf if pr.telf else None), **contact(pr))
		todict = lambda agenda: dict(
				id_agd = agenda.id_agd,
				fecha_msj = agenda.fecha_msj.isoformat(),
				fecha_con = agenda.fecha_con.isoformat(),
				tenor = agenda.mensaje.tenor,
				audio = agenda.mensaje.audio,
				**person(agenda.persona)
			)
		return dumps([todict(ag) for ag in Agenda.select(lambda ag: ag.enviado==False)])

@route('/mensajes/pdf_catalogo')
class TestReport(BaseHandler):
	@authenticated
	@asynchronous
	@coroutine
	def get(self):
		self.set_header('Content-type', 'application/pdf')
		params = cdict(
			img_path = path.join(path.dirname(self.settings['static_path']),'statics{}watermark.png'.format(sep)),
			title = u'Catálogo de Mensajes', user = self.current_user.persona,
			odate = to_ddmmyy(utc.now().date()), otime = utc.now().time().isoformat()[:8], portrait=False
		)
		render_type = lambda tp: 'Pre-Natal' if tp==1 else 'Post-Natal' if tp==2 else 'Pre-Promocional' if tp==3 else 'Post-Promocional' if tp==4 else 'Extraordinario'
		pm = ReportMaker(**params)
		datas = [['#', 'Tipo', 'Control', 'Tenor', 'Usuario']]
		with db_session:
			datas.extend([0, render_type(msg.tipo).upper(), msg.nro_control, msg.tenor, msg.usuario.persona.__str__()] for msg in messagesCrt.get_Catalogo())
		pm.parse_datatable(datas, cellsW={0:1.5,1:4,2:2.5,3:9,4:6})
		self.set_header('Content-Disposition', 'inline; filename="Catálogo_{}-{}.pdf"'.format(params.odate, params.otime))
		self.finish(pm.build_pdf())
"""
@route('/mensajes/renderpdf', name='renderpdf')
class PreviewPdf(BaseHandler):
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		self.set_header('Content-type', 'application/pdf')
		dt, hr, messages = to_ddmmyy(utc.now().date()), utc.now().time().isoformat()[:8], messagesCrt.get_Catalogo()
		params = dict(fecha=dt, hora=hr, messages=messages)
		pdf = create_pdf(self.render_string('mensajes/report_msg.html', **params))
		self.set_header('Content-Disposition', 'inline; filename="Catálogo_f{}h{}.pdf"'.format(dt, hr))
		#self.set_header('Content-Disposition', 'attachment; filename=Catálogo_f{}h{}.pdf'.format(dt, hr))
		self.finish(pdf)
		#self.finish('<embed type="application/pdf" src="data:application/pdf;base64,{}" style="width:100%;height:100%;"/>'.format(pdf.encode('base64').replace('\n','')))

@route('/mensajes/report', name='report')
class ReportEmbed(BaseHandler):
	@asynchronous
	@coroutine
	def get(self):
		#self.set_header('Content-type', 'application/pdf')
		client = AsyncHTTPClient()
		#response = yield Task(client.fetch, HTTPRequest('http://localhost/mensajes/renderpdf', method='GET'))
		response = yield client.fetch('http://localhost/mensajes/renderpdf')
		pdfencoded = response.body.encode('base64').replace('\n','')
		self.finish('<embed type="application/pdf" src="data:application/pdf;base64,{}" style="width:100%;height:100%;"/>'.format(pdfencoded))
"""