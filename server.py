#-*- coding: utf-8 -*-
import sys, logging, signal, time
reload(sys)
sys.setdefaultencoding('utf-8')

from os import environ
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import (define, parse_command_line, options)

from app import App_Server

define('debug', default=False, type=bool, help='Run in debug mode')
define('port', default=8080, type=int, help='Server port')
define('allowed_hosts', default='localhost:8080', multiple=True, help='Allowed hosts for cross domain connections')
define('localdb', default=True, type=bool, help='By default, the DB in local mode')

def shutdown(server):
	ioloop = IOLoop.instance()
	logging.info('Stopping server.')
	server.stop()
	def finalize():
		ioloop.stop()
		logging.info('Stopped.')
	ioloop.add_timeout(time.time() + .2, finalize)

if __name__ == '__main__':
	parse_command_line()
	server = HTTPServer(App_Server())
	server.listen(environ.get('PORT', options.port))
	signal.signal(signal.SIGINT, lambda sig, frame: shutdown(server))
	logging.info('Starting server on localhost:{}'.format(options.port))
	IOLoop.instance().start()