import logging

from wsgiref.simple_server import make_server

from apimock.bootstrap import bootstrap_api, setup_logger

setup_logger()

app = bootstrap_api()

server = make_server('0.0.0.0', 8080, app)
server.serve_forever()
