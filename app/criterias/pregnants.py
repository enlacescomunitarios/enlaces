#-*- coding: utf-8 -*-
#from datetime import (date, timedelta)
from ..tools import (to_date as _to_date, to_yymmdd as _to_yymmdd, PreNatal as _PreNatal)
from pony.orm import (db_session as _db_session, commit as _commit, flush as _flush, desc as _desc, count as _count)
from ..entities import (Comunidad as _Comunidad, Tipo as _Tipo, Etnia as _Etnia, Persona as _Persona, Embarazo as _Embarazo, Control as _Control, Defuncion as _Defuncion, Usuario as _Usuario)
from .controls import ControlsCriteria as _controlsCrt
from .agendas import AgendasCriteria as _agendasCrt
from .messages import MessagesCriteria as _messagesCrt

def pregnant_status(pregnant):
	prg = PregnantCriteria.current_pregnancy(pregnant.id_per)
	#prg = pregnant.embarazos.select(lambda: _Embarazo.activo==True).order_by(lambda: (_desc(_Embarazo.creado),)).first()
	if not(pregnant.activo) and not(pregnant.defuncion) and not(prg):
		return (0, u'Inhabilitada')
	elif pregnant.activo and not(pregnant.defuncion) and not(prg):
		return (1, u'Habilitada')
	elif pregnant.activo and not(pregnant.defuncion) and prg and not(prg.interrupcion):
		return (2, u'Gestando')
	elif pregnant.activo and not pregnant.defuncion and prg and prg.interrupcion and not prg.interrupcion.f_conf:
		return (3, u'Advertencia de interrupción') #pregnancy interrupt
	elif pregnant.activo and not pregnant.defuncion and prg and prg.interrupcion and prg.interrupcion.f_conf:
		return (4, u'Embarazo interrumpido')
	#elif pregnant.activo and pregnant.defuncion and not pregnant.defuncion.f_conf and prg and prg.interrupcion and not prg.interrupcion.f_conf:
	elif pregnant.activo and pregnant.defuncion and not pregnant.defuncion.f_conf:
		return (5, u'Advertencia de defunción')
	elif pregnant.activo and pregnant.defuncion and pregnant.defuncion.f_conf and prg and prg.interrupcion and prg.interrupcion.f_conf:
		return (6, u'Defunción con interrupción de embarazo')
	elif pregnant.activo and pregnant.defuncion and pregnant.defuncion.f_conf and not prg:
		return (7, u'Fallecida')
	else:
		return (-1, '')

class PregnantCriteria:
	@classmethod
	def total_womens(self):
		return _count(pr for pr in _Persona if pr.sexo=='f')
	@classmethod
	def total_pregnants(self):
		#q_filter = lambda pr, pg: pg.embarazada.id_per==pr.id_per and pg.activo and not pg.interrupcion
		return _count(pr for pr in _Persona for pg in pr.embarazos if pg.embarazada.id_per==pr.id_per and pg.activo and not pg.interrupcion)
	@classmethod
	def get_all(self):
		tp = _Tipo.get(id_tip=1)
		return (em for em in _Persona.select(lambda em: tp in em.tipos).order_by(lambda em: (em.comunidad, em.nombres, em.apellidos)))
	@classmethod
	def current_pregnancy(self, id_per):
		#return _select(pg for pr in _Persona for pg in pr.embarazos if pr.id_per==id_per and pg.activo).order_by(lambda pg: (_desc(pg.creado),)).first()
		return _Persona.get(id_per=id_per).embarazos.select(lambda emb: emb.activo).order_by(lambda emb: (_desc(emb.creado),)).first()
	@classmethod
	def save(self, form, user_id):
		try:
			#print _to_yymmdd(form.parto_prob)
			form.parto_prob = _to_yymmdd(form.parto_prob); form.f_nac = _to_yymmdd(form.f_nac)
			pp = _to_date(form.parto_prob)
			ctrls = _PreNatal(pp.year, pp.month, pp.day)
			check_pregnant = lambda: len([i for i in form.keys() if not i.startswith('c_')]) 
			check_contact = lambda: len([i for i in form.keys() if i.startswith('c_')])
			#print check_pregnant()
			#print check_contact()
			if check_pregnant()>5:
				em_fields = {k:v for k,v in form.iteritems() if not k.startswith('c_') and k not in ['id_com','id_etn','parto_prob']}
				#print em_fields
			cn_fields = lambda: {k.replace('c_',''):v for k,v in form.iteritems() if k.startswith('c_') and k!='c_id_etn'}
			with _db_session:
				tipos = [_Tipo.get(id_tip=1), _Tipo.get(id_tip=2)]
				com = _Comunidad.get(id_com=form.id_com)
				em_etn = _Etnia.get(id_etn=form.id_etn)
				if check_pregnant()>5:
					em = _Persona(comunidad=com, etnia=em_etn, tipos=[tipos[0]], **em_fields)
					_flush()
				else:
					em = _Persona.get(telf=form.telf)
					em.set(f_nac=form.f_nac, comunidad=com, etnia=em_etn)
					em.tipos += [tipos[0]]
					_flush()
				usuario = _Usuario.get(persona=user_id)
				#print "usuario: {}".format(usuario.__str__())
				embarazo = _Embarazo(embarazada=em, parto_prob=form.parto_prob, usuario=usuario)
				embarazo.controles += [_Control(embarazo=embarazo, nro_con=ctrl[0], fecha_con=ctrl[2]) for ctrl in ctrls.controls_dates()[::-1]]
				_flush()
				for cn in embarazo.controles:
					msg = _messagesCrt.get_byNumbControl(cn.nro_con)
					_agendasCrt.save(persona=em, mensaje=msg, fecha_con=cn.fecha_con)
				if check_contact()==1:
					contacto = _Persona.get(telf=form.c_telf)
					contacto.embarazadas += [em]
					if tipos[1] not in contacto.tipos:
						contacto.tipos += [tipos[1]]
					_flush()
				elif check_contact()>=6:
					cn_etnia = _Etnia.get(id_etn=form.c_id_etn)
					cnt = _Persona(comunidad=com, etnia=cn_etnia, tipos=[tipos[1]], **cn_fields())
					_flush()
					cnt.embarazadas += [em]
				_commit()
			return True
		except Exception, e:
			#raise e
			print e
			return False
	@classmethod
	def update(self, id_per, telf, nombres, apellidos, id_com, id_etn, f_nac, ci, c_telf, c_sexo, c_nombres=None, c_apellidos=None, c_id_per=None):
		f_nac = _to_yymmdd(f_nac); activo = True
		preg_form = dict([(k,v) for k,v in locals().iteritems() if not(k.startswith('_') or k.startswith('c_') or k.startswith('self') or k in ['id_com','id_etn','id_per'])])
		try:
			with _db_session:
				com = _Comunidad.get(id_com=id_com)
				etn = _Etnia.get(id_etn=id_etn)
				pregnant = _Persona.get(id_per=id_per)
				pregnant.set(comunidad=com, etnia=etn,**preg_form)
				if not(c_id_per is None):
					contact = _Persona.get(id_per=c_id_per)
					contact.set(sexo=c_sexo); _flush()
					if c_nombres is None:
						pregnant.contacto = contact; _flush()
					else:
						tmp = self.get_byCellphone(c_telf)
						if tmp:
							assert(tmp.id_per==pregnant.contacto.id_per)
						contact.set(telf=c_telf, nombres=c_nombres, apellidos=c_apellidos); _flush()
						pregnant.contacto = contact; _flush()
				else:
					contact = _Persona(telf=c_telf, nombres=c_nombres, apellidos=c_apellidos, sexo=c_sexo, tipos=[_Tipo.get(id_tip=2)])
					pregnant.contacto = contact
				_commit()
			return True
		except Exception, e:
			#raise e
			return False
	@classmethod
	def get_byCellphone(self, telf):
		return _Persona.get(telf=telf)
	@classmethod
	def death(self, id_per, fecha, f_notf, obs_notf, f_conf=None, obs_conf=None):
		f_death = lambda: dict(fecha=_to_yymmdd(fecha), f_notf=_to_yymmdd(f_notf), obs_notf=obs_notf.upper()) if f_conf is None else dict(fecha=_to_yymmdd(fecha), f_notf=_to_yymmdd(f_notf), obs_notf=obs_notf.upper(), f_conf=_to_yymmdd(f_conf), obs_conf=obs_conf.upper())
		try:
			with _db_session:
				em = _Persona.get(id_per=id_per)
				if f_conf:
					em.telf = None #em.contacto = None
					if not em.embarazadas.is_empty():
						em.embarazadas.clear()
					if not em.agendas.is_empty():
						_agendasCrt.delete_agendas(em)
				death = _Defuncion(embarazada=em, **f_death())
				c_prg = self.current_pregnancy(id_per)
				if c_prg:
					death.embarazo = c_prg
					if f_conf:
						_controlsCrt.delete_controls(c_prg)
				_commit()
			return True
		except Exception, e:
			#raise e
			return False
	@classmethod
	def confirm_death(self, id_def, f_conf, obs_conf):
		try:
			with _db_session:
				death = _Defuncion.get(id_def=id_def)
				death.set(f_conf=_to_yymmdd(f_conf), obs_conf=obs_conf)
				death.embarazada.telf = None #death.embarazada.contacto = None
				if not death.embarazada.embarazadas.is_empty():
					death.embarazada.embarazadas.clear()
				if death.embarazo:
					_controlsCrt.delete_controls(death.embarazo)
				if not death.embarazada.agendas.is_empty():
					_agendasCrt.delete_agendas(death.embarazada)
				_commit()
			return True
		except Exception, e:
			#raise e
			return False
	@classmethod
	def del_death(self, id_def):
		try:
			with _db_session:
				death = _Defuncion.get(id_def=id_def)
				death.delete()
				_commit()
			return True
		except Exception, e:
			#raise e
			return False
	@classmethod
	def delete(self, id_per):
		try:
			with _db_session:
				pr = _Persona.get(id_per=id_per)
				pr.activo = False
				if not pr.agendas.is_empty():
					_agendasCrt.delete_agendas(pr)
				_commit()
			return False
		except Exception, e:
			#raise e
			return True