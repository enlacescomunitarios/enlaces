#-*- coding: utf-8 -*-
from __future__ import absolute_import
#from tornado.web import authenticated
from calendar import leapdays
from datetime import timedelta
from ..tools import (route, BaseHandler, utcDateTime, to_ddmmyy)
from pony.orm import (db_session,)
from ..entities import (Persona, Defuncion, Tipo)
from ..criterias import (pregnantCrt, pregnant_status)
from json import (dumps,)

def find_pregnant(pregnant):
	tp = Tipo.get(id_tip=1)
	for tipo in pregnant.tipos:
		if tipo==tp:
			return True
	else:
		return False

def min_age():
	today = utcDateTime().now().date()
	leaps = leapdays((today.year-12), today.year)
	withoutleaps = 12 - leaps
	return today - timedelta(days=((withoutleaps*365)+(leaps*364)))

@route('/embarazadas/gestion')
class Gestion_Embarazadas(BaseHandler):
	@db_session
	def get(self):
		embarazadas = pregnantCrt.get_all()
		self.render('embarazadas/gestion.html', embarazadas=embarazadas, emb_status=pregnant_status)

@route('/embarazadas/nueva_embarazada')
class Nueva_Embarazada(BaseHandler):
	def get(self):
		params = dict(utc=self.get_utc(), to_ddmmyy=to_ddmmyy, min_age=min_age)
		self.render('embarazadas/nueva_embarazada.html', **params)
	def post(self):
		self.set_header('Content-type', 'application/json')
		#print self.form2Dict().keys()
		success = pregnantCrt.save(self.form2Dict(), self.current_user.id)
		self.write(dumps(success))

@route('/embarazadas/modificar_embarazada')
class Modificar_Embarazada(BaseHandler):
	@db_session
	def get(self):
		pr = Persona.get(**self.form2Dict())
		f_comunidad = lambda: dict(id_com=pr.comunidad.id_com, id_mup=pr.comunidad.municipio.id_mup, id_red=pr.comunidad.municipio.red_salud.id_red) if pr.comunidad else {'id_con':None}
		checkfields = dumps(dict(is_pregnant=find_pregnant(pr), id_etn=pr.etnia.id_etn, **f_comunidad()))
		self.render('embarazadas/modificar_embarazada.html', pr=pr, checkfields=checkfields, to_ddmmyy=to_ddmmyy)
	def post(self):
		self.set_header('Content-type', 'application/json')
		flag = pregnantCrt.update(**self.form2Dict())
		self.write(dumps(flag))

@route('/embarazadas/defuncion')
class Defuncion_Embarazada(BaseHandler):
	@db_session
	def get(self):
		em = Persona.get(**self.form2Dict())
		self.render('embarazadas/defuncion.html',em=em, to_ddmmyy=to_ddmmyy)
	def post(self):
		self.set_header('Content-type', 'application/json')
		flag = pregnantCrt.death(**self.form2Dict())
		self.write(dumps(flag))

@route('/embarazadas/conf_defuncion')
class ConfDefuncion_Embarazada(BaseHandler):
	@db_session
	def get(self):
		death = Defuncion.get(embarazada=self.form2Dict().id_per)
		self.render('embarazadas/conf_defuncion.html', death=death, to_ddmmyy=to_ddmmyy)
	def post(self):
		self.set_header('Content-type', 'application/json')
		flag = pregnantCrt.confirm_death(**self.form2Dict())
		self.write(dumps(flag))

@route('/embarazadas/del_defuncion')
class InterrDefunction(BaseHandler):
	def post(self):
		self.set_header('Content-type', 'application/json')
		flag = pregnantCrt.del_death(**self.form2Dict())
		self.write(dumps(not flag))

@route('/embarazadas/eliminar')
class EliminarEmbarazada(BaseHandler):
	def post(self):
		self.set_header('Content-type', 'application/json')
		self.write(dumps(pregnantCrt.delete(**self.form2Dict())))