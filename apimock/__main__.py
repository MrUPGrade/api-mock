import logging

from wsgiref.simple_server import make_server

from apimock.bootstrap import bootstrap_api

logging.basicConfig(level=logging.DEBUG)

api = bootstrap_api()

server = make_server('0.0.0.0', 8080, api)
server.serve_forever()
