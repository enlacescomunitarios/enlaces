#-*- coding: utf-8 -*-
from __future__ import absolute_import
from ..tools import (route, BaseHandler, conf)
from tornado.web import (authenticated, asynchronous)
from pony.orm import (db_session, select, desc)
from ..entities import (Mensaje, Agenda)
from ..criterias import (messagesCrt, agendaCrt, personsCrt)
from json import dumps
from os import path
from fabric.api import (env, put, run)

@route('/mensajes/gestion')
class MensajesGestion(BaseHandler):
	@authenticated
	@asynchronous
	@db_session
	def get(self):
		mensajes = select(msg for msg in Mensaje if msg.tipo!=5).order_by(lambda msg: (msg.tipo, msg.nro_control, desc(msg.creado)))
		self.render('mensajes/gestion.html', mensajes=mensajes)

@route('/mensajes/adicionar_msj')
class AdicionarMsj(BaseHandler):
	@authenticated
	@asynchronous
	def get(self):
		self.render('mensajes/adicionar_msj.html')
	@asynchronous
	def post(self):
		self.set_header('Content-type', 'application/json')
		form = self.form2Dict()
		fileau = self.request.files['audio'][0]['body']
		if fileau:
			pathfile = '{}{}audio{}{}'.format(self.settings['static_path'], path.sep, path.sep, renameaudio(form.tipo, form.nro_control))
			with open(pathfile, 'wb') as fl:
				fl.write(fileau)
				try:
					self.to_asterisk(pathfile)
				except Exception, e:
					#print e
					pass
		self.write(dumps(messagesCrt.save(form=form, id_user=self.current_user.id)))
		self.finish()
	def to_asterisk(self, file):
		env.user = conf.asterisk.user
		env.password = conf.asterisk.password
		env.host_string = conf.asterisk.ip
		put(file, conf.asterisk.destination)

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
	@asynchronous
	@db_session
	def get(self):
		persons = personsCrt.get_All()
		self.render('mensajes/sendsms.html', personas=persons)
	@asynchronous
	@db_session
	def post(self):
		self.set_header('Content-type', 'application/json')
		form = self.form2Dict(); form.tipo = 5
		if form.has_key('id_per') and form.has_key('telf'):
			del form.id_per, form.telf
		#print form
		personas = [(id_per, telf) for id_per, telf in zip(self.get_arguments('id_per'), self.get_arguments('telf'))]
		msg = messagesCrt.save(form=form, id_user=self.current_user.id, default=False)
		if msg:
			self.sendsms(msg, personas)
		self.write(dumps(True));
		self.finish()
	def sendsms(self, msg, persons):
		env.user = conf.cedes.user
		env.password = conf.cedes.password
		env.host_string = conf.cedes.ip
		for pr in persons:
			try:
				run('echo "{}" | gsmsendsms -d /dev/ttyUSB0 -b 19200 +591{}'.format(msg.tenor, pr[1]))
				persona = personsCrt.get_byId(id_per=pr[0])
				agendaCrt.save(persona=persona, mensaje=msg)
			except Exception, e:
				print e
				pass

def renameaudio(numb_status, numb_control, ext='mp3'):
	status = ['prenatal','postnatal','prom_prenatal','prom_postnatal','extraordinario']
	return '{}_{:02}.{}'.format(status[int(numb_status)-1], int(numb_control), ext)

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
	@db_session
	def get(self):
		self.set_header('Content-type', 'application/json')
		apikey = self.application.settings['cookie_secret']
		try:
			query = self.form2Dict().apikey.encode('utf-8')
			if query == apikey:
				agendas = [self.parse_agenda(ag) for ag in Agenda.select(lambda ag: ag.enviado==False)]
				self.write(dumps(agendas))
			else:
				self.write('Error')
		except Exception, e:
			self.write('Error')
		self.finish()
	def parse_agenda(self, agenda):
		return dict(
				fecha_msj = agenda.fecha_msj.isoformat(),
				fecha_con = agenda.fecha_con.isoformat(),
				persona = agenda.persona.__str__(),
				p_telf = agenda.persona.telf or '',
				contacto = agenda.persona.contacto.__str__(),
				c_telf = agenda.persona.contacto.telf,
				tenor = agenda.mensaje.tenor if agenda.persona.telf else 'para {}: {}'.format(agenda.persona.__str__(), agenda.mensaje.tenor),
			)