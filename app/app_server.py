#-*- coding: utf-8 -*-
from tornado.options import options as _options
from tornado.web import Application as _App
from os.path import (join as _join)
from . import views as _views
from .tools import (projdir as _projdir, conf as _conf, url_handlers as _url_handlers)
from .entities import db

class App_Server(_App):
	def __init__(self):
		db.bind('postgres', **_conf.dbconf)
		db.generate_mapping(create_tables=True)
		settings = dict(
			static_path = _join(_projdir, 'statics'),
			static_hash_cache = not _options.debug,
			template_path = _join(_projdir, 'templates'),
			compile_template_cache = not _options.debug,
			#compress_response = True,
			cookie_secret = 'NGM0NTRkNDIyZDRiNDg0MTU3NDE1ODNhNDU2YzYxNjM2NTcz',
			xsrf_cookies = True,
			login_url = '/login',
			server_traceback = _options.debug,
			debug = _options.debug
		)
		#print url_handlers
		super(App_Server, self).__init__(handlers=_url_handlers, **settings)