#-*- coding: utf-8 -*-
from time import sleep
from json import loads
from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient

AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

apikey = 'NGM0NTRkNDIyZDRiNDg0MTU3NDE1ODNhNDU2YzYxNjM2NTcz'

def test():
	link = 'http://localhost/api/getagenda?apikey={}'.format(apikey)
	aclient = AsyncHTTPClient()
	aclient.fetch(link, expect_100_continue=True, request_timeout=120.0, callback=handle_request)
	IOLoop.current().start()

def handle_request(response):
	#print dir(response)
	#for i in response.headers.get_all():
	#	print i
	if response.error:
		print "Error:", response.error
	else:
		for ag in loads(response.body):
			print '{} -- {}'.format(ag['persona'], ag['p_telf'])
		IOLoop.current().stop()

if __name__ == '__main__':
	for i in range(1000):
		test()
		sleep(.7)