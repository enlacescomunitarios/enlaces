#-*- coding: utf-8 -*-
from tornado.gen import coroutine
from tornado.web import (authenticated, asynchronous)
from ..tools import (route, BaseHandler, utc, to_ddmmyy, cdict, ReportMaker)
from pony.orm import db_session
from ..criterias import pregnantCrt, childrensCrt
from os import path, sep
from json import dumps

@route('/reportes')
class Reportes(BaseHandler):
	@authenticated
	@asynchronous
	@coroutine
	def get(self):
		self.render('reportes/reportes.html')
	@authenticated
	@asynchronous
	@coroutine
	def post(self):
		self.set_header('Content-type', 'application/json')
		params = cdict(
			img_path = path.join(path.dirname(self.settings['static_path']),'statics{}watermark.png'.format(sep)),
			title = u'Reporte General', user = self.current_user.persona,
			odate = to_ddmmyy(utc.now().date()), otime = utc.now().time().isoformat()[:8], portrait=False
		)
		pm = ReportMaker(**params)
		pm.heading_content('Reporte Global', align='justify', sep=.5)
		datas = [[u'Establecimientos de Salud',u'Mujeres Registradas',u'Mujeres en Gestación',u'Controles Pre-Natales',u'Defunciones Maternas',u'Recién Nacidos',u'Controles Post-Natales',u'Embarazos de Riesgo']]
		pm.parse_datatable(datas, cellsW={0:4.5,1:2.7,2:2.7,3:2.7,4:2.7,5:2.7,6:2.7,7:2.7})
		json_response = dict(
			pdf = pm.build_pdf().encode('base64').replace('\n','')
		)
		self.set_header('Content-Disposition', u'inline; filename="Reporte_{}-{}.pdf"'.format(params.odate, params.otime))
		self.finish(dumps(json_response))