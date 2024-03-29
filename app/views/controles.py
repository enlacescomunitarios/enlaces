#-*- coding: utf-8 -*-
from tornado.web import asynchronous
from tornado.gen import coroutine
from ..tools import (route, BaseHandler, to_ddmmyy)
from pony.orm import (db_session, commit)
from ..entities import (Embarazo, Recien_Nacido, Control, Defuncion)
from ..criterias import (controlsCrt, pregnancy_status, childrensCrt)
from json import dumps

@route('/controles/gestion')
class Controles_Gestion(BaseHandler):
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		form = self.form2Dict()
		if form.has_key('id_emb'):
			em = Embarazo.get(**form)
			params = dict(
				pr = em.embarazada,
				em = em,
				pregnancy_status = pregnancy_status,
				controles = controlsCrt.getbyPregnancy(em.id_emb),
				to_ddmmyy = to_ddmmyy
			)
			self.render('controles/gestion.html', **params)
		else:
			neo = Recien_Nacido.get(**form)
			params = dict(
				neo = neo,
				controles = controlsCrt.getbyChild(neo.id_rcn),
				to_ddmmyy = to_ddmmyy
			)
			self.render('controles/neo_controles.html', **params)

@route('/controles/control_asistencia')
class Control_Asistencia(BaseHandler):
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		ct = Control.get(**self.form2Dict())
		if ct.embarazo:
			self.render('controles/asistencia.html', ct=ct)
		else:
			self.render('controles/neo_asistencia.html', ct=ct)
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		form = self.form2Dict()
		with db_session:
			ct = Control.get(id_cnt=form.id_cnt)
			if ct:
				del form['id_cnt']; form.asistido = eval(form.asistido)
				ct.set(**form)
				commit()
		self.finish(dumps(True if ct else False))

@route('/controles/modificar_neo')
class ModificarNeo(BaseHandler):
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		neo = Recien_Nacido.get(**self.form2Dict())
		self.render('controles/neo_modificar.html', neo=neo, to_ddmmyy=to_ddmmyy)
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		self.finish(dumps(childrensCrt.update(**self.form2Dict())))

@route('/controles/neo_defuncion')
class NeoDefuncion(BaseHandler):
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		neo = Recien_Nacido.get(**self.form2Dict())
		self.render('controles/neo_defuncion.html', neo=neo)
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		self.finish(dumps(childrensCrt.death(**self.form2Dict())))

@route('/controles/neo_confirmDef')
class NeoConfirmarDef(BaseHandler):
	@db_session
	@asynchronous
	@coroutine
	def get(self):
		death = Defuncion.get(**self.form2Dict())
		self.render('controles/neo_confirmDef.html', death=death, to_ddmmyy=to_ddmmyy)
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		self.finish(dumps(childrensCrt.confirm_death(**self.form2Dict())))

@route('/controles/eliminar_defuncion')
class NeoEliminarDef(BaseHandler):
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		self.finish(dumps(childrensCrt.delete_death(**self.form2Dict())))