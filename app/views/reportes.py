#-*- coding: utf-8 -*-
from tornado.gen import coroutine
from tornado.web import (authenticated, asynchronous)
from ..tools import (route, BaseHandler, utc, to_ddmmyy, cdict, ReportMaker)
from ..criterias import DatasReport
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
		DatasReport.global_Report(pm)
		json_response = cdict(
			pdf = pm.build_pdf().encode('base64').replace('\n',''),
			filename = u'Reporte_{}-{}.pdf'.format(params.odate, params.otime)
		)
		self.set_header('Content-Disposition', u'inline; filename={}'.format(json_response.filename))
		self.finish(dumps(json_response))