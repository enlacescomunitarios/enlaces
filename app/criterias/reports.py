#-*- coding: utf-8 -*-
from pony.orm import db_session as _db_session, select as _select, desc as _desc
from ..entities import Mensaje as _Msg, Red_Salud as _Red, Persona as _Per

class _Index(object):
	def __init__(self):
		self.idx = 0
	def counter(self):
		self.idx += 1
		return self.idx
	def reset(self):
		self.idx = 0

sumCol = lambda col, dtMatrix: reduce(lambda x,y: x+y, [i[col] for i in dtMatrix]) if len(dtMatrix) else 0

def totalRow(dtMatrix, strTotal=u'Totales'):
	totals = [[strTotal]]
	totals[0].extend([sumCol(i, dtMatrix[1:]) for i in range(1, len(dtMatrix[0]))])
	return totals

class _Womens:
	def prenants_by_community(self, id_com):
		return _select(pr for pr in _Per if pr.sexo=='f' and pr.comunidad.id_com==id_com)
	@classmethod
	def womens(cls, id_com):
		return cls().prenants_by_community(id_com=id_com).count()
	@classmethod
	def in_pregnancy(cls, id_com):
		count, qfilter = 0, lambda embarazos: embarazos.select(lambda emb: emb.activo and not emb.interrupcion).order_by(lambda emb: (_desc(emb.creado),)).first()
		for pr in cls().prenants_by_community(id_com=id_com):
			if qfilter(pr.embarazos):
				count += 1
		return count
	@classmethod
	def pre_natals(cls, id_com):
		count, qfilter = 0, lambda controles: controles.select(lambda crt: crt.asistido).count()
		for pr in cls().prenants_by_community(id_com=id_com):
			for emb in pr.embarazos:
				count += qfilter(emb.controles)
		return count
	@classmethod
	def mothers_death(cls, id_com):
		count = 0
		for pr in cls().prenants_by_community(id_com=id_com):
			if pr.defuncion and pr.defuncion.f_conf:
				count += 1
		return count
	@classmethod
	def childrens(cls, id_com):
		count = 0
		for pr in cls().prenants_by_community(id_com=id_com):
			for emb in pr.embarazos:
				if emb.parto_inst:
					count += emb.recien_nacidos.select().count()
		return count
	@classmethod
	def post_natals(cls, id_com):
		count, qfilter = 0, lambda controles: controles.select(lambda crt: crt.asistido).count()
		for pr in cls().prenants_by_community(id_com=id_com):
			for emb in pr.embarazos:
				for ch in emb.recien_nacidos:
					count += qfilter(ch.controles)
		return count
	@classmethod
	def childrens_death(cls, id_com):
		count = 0
		for pr in cls().prenants_by_community(id_com=id_com):
			for emb in pr.embarazos:
				for ch in emb.recien_nacidos:
					if ch.defuncion and ch.defuncion.f_conf:
						count += 1
		return count

class DatasReport:
	@classmethod
	def get_Catalogo(cls):
		idx = _Index()
		type_str = lambda tp: 'Pre-Natal' if tp==1 else 'Post-Natal' if tp==2 else 'Pre-Promocional' if tp==3 else 'Post-Promocional' if tp==4 else 'Extraordinario'
		parse_data = lambda msg: [idx.counter(), type_str(msg.tipo).upper(), msg.nro_control, msg.tenor, msg.usuario.persona.__str__()]
		data_matrix = [['#', 'Tipo', 'Control', 'Tenor', 'Usuario']]
		with _db_session:
			data_matrix.extend([parse_data(msg) for msg in _Msg.select(lambda msg: msg.tipo>=1 and msg.tipo<=4).order_by(lambda msg: (msg.tipo, msg.nro_control))])
		return data_matrix
	@classmethod
	@_db_session
	def global_Report(cls, repr_maker):
		wms, rd_idx, mup_idx = _Womens(), _Index(), _Index()
		for rd in _Red.select(lambda rd: rd.activo==True).order_by(lambda rd: (rd.nombre,)):
			repr_maker.heading_content(u'{}.- Red de Salud: {}'.format(rd_idx.counter(), rd.__str__()), align='justify', sep=.3)
			for mup in rd.municipios.select(lambda mup: mup.activo).order_by(lambda mup: (mup.nombre,)):
				repr_maker.heading_content(u'{}.{}.- Municipio: {}'.format(rd_idx.idx, mup_idx.counter(), mup.__str__()), align='justify', sep=.3)
				table = [[u'Comunidad',u'Mujeres Registradas',u'Mujeres en Gestación',u'Embarazos de Riesgo',u'Controles Pre-Natales',u'Defunciones Maternas',u'Recién Nacidos',u'Controles Post-Natales',u'Defunciones R. Nacidos']]
				for com in mup.comunidades.select(lambda com: com.activo).order_by(lambda com: (com.nombre,)):
					table.extend([[com.__str__(), wms.womens(com.id_com), wms.in_pregnancy(com.id_com),0, wms.pre_natals(com.id_com), wms.mothers_death(com.id_com), wms.childrens(com.id_com), wms.post_natals(com.id_com), wms.childrens_death(com.id_com)]])
				table.extend(totalRow(table, strTotal=u'Sub-Totales'))
				repr_maker.parse_datatable(table, footer=True, cellsW={0:4.5,1:2.4,2:2.4,3:2.4,4:2.4,5:2.4,6:2.4,7:2.4,8:2.4})
				mup_idx.reset()