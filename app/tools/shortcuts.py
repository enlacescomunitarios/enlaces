#-*- coding: utf-8 -*-
from . import cdict
from . import utcDateTime as _utcDateTime
from tornado.web import RequestHandler as _RequestHandler
from mako.lookup import TemplateLookup as _TemplateLookup
from json import loads as _loads
from datetime import (date as _date, datetime as _datetime)

def getLocals(obj):
	#return {k:v for k,v in obj.iteritems() if not(k.startswith('_') or k.startswith('self'))}
	return cdict([(k,v) for k,v in obj.iteritems() if not(k.startswith('_') or k.startswith('self'))])

def _form2Dict(obj):
	#return {k:obj.get_argument(k) for k in obj.request.arguments.iterkeys() if(k != '_xsrf')}
	return cdict([(k,obj.get_argument(k)) for k in obj.request.arguments.iterkeys() if not(k.startswith('_'))])

def _dict2Obj(o_name, **params):
	return type(o_name, (object,), params)

def _obj2Dict(obj):
	check_values = lambda v: v.isoformat() if isinstance(v,_date) else '{} {}'.format(v._date().isoformat(),v.time().isoformat()[:8]) if isinstance(v,_datetime) else v
	#return {k:check_values(v) for k,v in obj.to_dict().iteritems()}
	return cdict([(k,check_values(v)) for k,v in obj.to_dict().iteritems()])

def _cookie_user2Obj(obj, cookie_name):
	tmp = obj.get_secure_cookie(cookie_name)
	try:
		tmp = _loads(tmp)
	except TypeError:
		tmp = eval(tmp) if tmp else None
	return _dict2Obj("User", **tmp) if tmp else None

class BaseHandler(_RequestHandler):
	def initialize(self):
		self.lookup = _TemplateLookup(directories=[self.get_template_path()], input_encoding='utf-8', output_encoding='utf-8')
	def render_string(self, template_path, **kwargs):
		template, namespace = self.lookup.get_template(template_path), self.get_template_namespace()
		namespace.update(kwargs); namespace.update(dict(format_exceptions=True))
		return template.render(**namespace)
	def render(self, template_path, **kwargs):
		self.finish(self.render_string(template_path, **kwargs))
	def get_current_user(self):
		return _cookie_user2Obj(self, "user")
	def get_utc(self):
		return _utcDateTime()
	def form2Dict(self):
		return _form2Dict(self)
	def obj2Dict(self):
		return _obj2Dict(self)