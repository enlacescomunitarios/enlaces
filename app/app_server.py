#-*- coding: utf-8 -*-
from __future__ import absolute_import
from tornado.options import options as _options
from tornado.web import Application as _App
from os.path import (join as _join)
from . import views as _views
from .tools import (projdir as _projdir, conf as _conf, url_handlers as _url_handlers)
from .entities import db

_load_dbconf = lambda flag: _conf.developdb if flag else _conf.productiondb

class App_Server(_App):
	def __init__(self):
		db.bind('postgres', **_load_dbconf(_options.localdb))
		db.generate_mapping(create_tables=True)
		settings = dict(
			static_path = _join(_projdir, 'statics'),
			static_hash_cache = not _options.debug,
			template_path = _join(_projdir, 'templates'),
			compile_template_cache = not _options.debug,
			cookie_secret = 'NTQ2NTZjNjU1MzYxNmM3NTY0\n',
			xsrf_cookies = True,
			login_url = '/login',
			server_traceback = True,
			debug = True
		)
		#print url_handlers
		super(App_Server, self).__init__(handlers=_url_handlers, **settings)