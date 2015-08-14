#-*- coding: utf-8 -*-
from tornado.web import asynchronous
from tornado.gen import coroutine
from ..tools import (route, BaseHandler, to_ddmmyy)
from pony.orm import (db_session, desc)
from ..entities import (Embarazo, Persona, Recien_Nacido, Defuncion)
from ..criterias import (pregnanciesCrt, pregnancy_status, pregnant_status, pregnancyWeek)
from json import dumps

@route('/embarazos/gestion')
class Embarazos_Gestion(BaseHandler):
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		pr = Persona.get(**self.form2Dict())
		embarazos = pregnanciesCrt.get_all(pr.id_per)
		neonatos = [neo for neo in Recien_Nacido.select(lambda neo: neo.embarazo.embarazada.id_per==pr.id_per).order_by(lambda neo: (desc(neo.creado),))]
		#status = pregnant_status(pr)
		#self.render('embarazos/gestion.html', pr=cdict(id=pr.id_per,name=pr.__str__(),status=status), embarazos=embarazos, pregnancy_status=pregnancy_status, utc=self.get_utc())
		params = dict(
			pr=pr,
			embarazos=embarazos,
			neonatos=neonatos,
			pregnant_status=pregnant_status,
			pregnancy_status=pregnancy_status,
			to_ddmmyy = to_ddmmyy,
			pregnancyWeek = pregnancyWeek
		)
		self.render('embarazos/gestion.html', **params)

@route('/embarazos/reg_parto')
class Reg_Parto(BaseHandler):
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		em = Embarazo.get(**self.form2Dict())
		self.render('embarazos/reg_parto.html', em=em, utc=self.get_utc(), to_ddmmyy=to_ddmmyy)
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		success = pregnanciesCrt.childbirth(self)
		self.finish(dumps(success))

@route('/embarazos/nuevo_embarazo')
class Nuevo_Embarazo(BaseHandler):
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		pr = Persona.get(**self.form2Dict())
		self.render('embarazos/nuevo_embarazo.html', pr=pr, utc=self.get_utc(), to_ddmmyy=to_ddmmyy)
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		success = pregnanciesCrt.save(id_user=self.current_user.id,**self.form2Dict())
		self.finish(dumps(success))

@route('/embarazos/interrumpir')
class Interrumpir_Embarazo(BaseHandler):
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		em = Embarazo.get(**self.form2Dict())
		self.render('embarazos/interrumpir.html', em=em, utc=self.get_utc(), to_ddmmyy=to_ddmmyy)
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		flag = pregnanciesCrt.interrupt(**self.form2Dict())
		self.finish(dumps(flag))

@route('/embarazos/conf_interr')
class Conf_Interrupcion(BaseHandler):
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		death = Defuncion.get(embarazo=self.form2Dict().id_emb)
		self.render('embarazos/conf_interr.html', death=death, utc=self.get_utc(), to_ddmmyy=to_ddmmyy)
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		flag = pregnanciesCrt.conf_interrupt(**self.form2Dict())
		self.finish(dumps(flag))

@route('/embarazos/del_interr')
class Del_Interrupcion(BaseHandler):
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		flag = pregnanciesCrt.del_interrupt(**self.form2Dict())
		self.finish(dumps(not flag))