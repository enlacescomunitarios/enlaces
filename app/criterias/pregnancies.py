#-*- coding: utf-8 -*-
from __future__ import absolute_import
from pony.orm import (db_session as _db_session, commit as _commit, flush as _flush, select as _select, desc as _desc)
from ..entities import (Embarazo as _Embarazo, Control as _Control, Recien_Nacido as _NewBorn, Persona as _Persona, Usuario as _Usuario, Defuncion as _Defuncion)
from ..tools import (to_date as _to_date, to_yymmdd as _to_yymmdd, PreNatal as _PreNatal, PostNatal as _PostNatal)
from .controls import ControlsCriteria as _controlsCrt

def pregnancy_status(prg):
	pregnant = prg.embarazada
	if not prg.activo and not(prg.interrupcion):
		return (0, u'Embarazo Culminado')
	if pregnant.activo and not pregnant.defuncion and prg and not prg.interrupcion:
		return (1, u'Gestando')
	elif pregnant.activo and not pregnant.defuncion and prg and prg.interrupcion and not prg.interrupcion.f_conf:
		return (2, u'Advertencia')
	elif pregnant.activo and pregnant.defuncion and not pregnant.defuncion.f_conf and prg and prg.interrupcion and not prg.interrupcion.f_conf:
		return (3, u'Advertencia')
	elif prg and prg.interrupcion and prg.interrupcion.f_conf:
		return (4, u'Embarazo Interrumpido')
	else:
		return (-1, '')

class PregnanciesCriteria:
	@classmethod
	def get_all(self, id_per):
		return _select(em for em in _Embarazo if em.embarazada.id_per==id_per).order_by(lambda em: (_desc(em.parto_prob),))
	@classmethod
	def save(self, id_per, parto_prob, id_user):
		try:
			parto_prob = _to_yymmdd(parto_prob)
			pp = _to_date(parto_prob)
			ctrls = _PreNatal(pp.year, pp.month, pp.day)
			with _db_session:
				pregnant = _Persona.get(id_per=id_per)
				usuario = _Usuario.get(persona=id_user)
				pregnacy = _Embarazo(embarazada=pregnant, parto_prob=parto_prob, usuario=usuario)
				pregnacy.controles += [_Control(embarazo=pregnacy, nro_con=ctrl[0], fecha_con=ctrl[2]) for ctrl in ctrls.controls_dates()[::-1]]
				_commit()
			return True
		except Exception, e:
			#raise e
			return False
	@classmethod
	def childbirth(self, obj):
		try:
			pinst = _to_date(_to_yymmdd(obj.get_argument('parto_inst')))
			ctrls = _PostNatal(pinst.year, pinst.month, pinst.day)
			#f_emb = lambda: dict(parto_inst=obj.get_argument('parto_inst'),tipo=obj.get_argument('tipo'),observacion=obj.get_argument('observacion'))
			f_emb = lambda: dict(parto_inst=_to_yymmdd(obj.get_argument('parto_inst')),tipo=obj.get_argument('tipo'))
			pesos, nombres, apellidos = obj.get_arguments('peso'), obj.get_arguments('nombres'), obj.get_arguments('apellidos')
			sexos = [obj.get_argument('sexo{}'.format(s)) for s in xrange(len(nombres))] if len(nombres)>1 else [obj.get_argument('sexo0')]
			with _db_session:
				em = _Embarazo.get(id_emb=obj.get_argument('id_emb'))
				em.set(activo=False, **f_emb())
				_flush()
				controls = lambda: [_Control(tipo=u'Post-Natal', nro_con=ctrl[0], fecha_con=ctrl[1]) for ctrl in ctrls.controls_date()]
				em.recien_nacidos += [_NewBorn(embarazo=em,peso=nb[0],sexo=nb[1],nombres=nb[2],apellidos=nb[3],controles=controls()) for nb in zip(pesos,sexos,nombres,apellidos)]
				_controlsCrt.delete_controls(em)
				#em.controles += [_Control(embarazo=em, tipo=u'Post-Natal', nro_con=ctrl[0], fecha_con=ctrl[1]) for ctrl in ctrls.controls_date()]
				_commit()
			return True
		except Exception, e:
			#raise e
			return False
	@classmethod
	def interrupt(self, id_emb, fecha, f_notf, obs_notf, f_conf=None, obs_conf=None):
		f_interr = lambda: dict(fecha=_to_yymmdd(fecha), f_notf=_to_yymmdd(f_notf), obs_notf=obs_notf.upper()) if f_conf is None else dict(fecha=_to_yymmdd(fecha), f_notf=_to_yymmdd(f_notf), obs_notf=obs_notf.upper(), f_conf=_to_yymmdd(f_conf), obs_conf=obs_conf.upper())
		try:
			with _db_session:
				em = _Embarazo.get(id_emb=id_emb)
				if f_conf:
					_controlsCrt.delete_controls(em)
					em.activo = False
				p_interrupt = _Defuncion(embarazo=em, **f_interr())
				_commit()
			return True
		except Exception, e:
			#raise e
			return False
	@classmethod
	def conf_interrupt(self, id_def, f_conf, obs_conf):
		try:
			with _db_session:
				interr = _Defuncion.get(id_def=id_def)
				interr.set(f_conf=_to_yymmdd(f_conf), obs_conf=obs_conf.upper())
				interr.embarazo.activo = False
				_controlsCrt.delete_controls(interr.embarazo)
				_commit()
			return True
		except Exception, e:
			#raise e
			return False
	@classmethod
	def del_interrupt(self, id_def):
		try:
			with _db_session:
				interr = _Defuncion.get(id_def=id_def)
				interr.delete()
				_commit()
			return True
		except Exception, e:
			#raise e
			return False