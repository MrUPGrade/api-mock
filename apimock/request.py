import json
from datetime import datetime
from pathlib import Path

import attr

from logging import getLogger

debug_log = getLogger('debug')


@attr.s
class RequestData:
    uri = attr.ib(init=False)
    method = attr.ib(init=False)
    headers = attr.ib(init=False, default=attr.Factory(dict))

    def to_dict(self):
        return attr.asdict(self)


class RequestParser:
    def process(self, request):
        uri = request.relative_uri.rstrip(request.query_string).rstrip('?').lstrip('/')
        debug_log.debug('URI: %s', uri or '/')

        request_data = RequestData()
        request_data.uri = uri
        request_data.method = request.method.lower()
        request_data.headers = dict(request.headers)

        return request_data


class SimpleRequestLogger:
    def __init__(self, root_path):
        self.root_path = root_path

    def process(self, request_data, request):
        p = self.root_path / request_data.uri

        if not p.exists():
            p.mkdir(parents=True)

        p = p / ('%s.json' % datetime.now().strftime('%Y%m%d%H%M%S'))

        with p.open('w') as f:
            json.dump(request_data.to_dict(), f)
