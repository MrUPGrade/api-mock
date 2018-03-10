import json
from datetime import datetime
from logging import getLogger

import attr

debug_log = getLogger('debug')


@attr.s
class RequestData:
    uri = attr.ib(init=False)
    method = attr.ib(init=False)
    headers = attr.ib(init=False, default=attr.Factory(dict))
    _dt = attr.ib(init=False, default=attr.Factory(datetime.now))

    @property
    def id(self):
        return '%s_%s' % (self.method, self._dt.strftime('%Y%m%d_%H%M%S_%f'))

    def _filter(self, attr, value):
        if attr.name in ('_dt'):
            return False

        return True

    def to_dict(self):
        return attr.asdict(self, filter=self._filter)


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

    def _preapre_data(self, request_data):
        data = {}
        data['request'] = request_data.to_dict()

        return data

    def process(self, request_data, request):
        p = self.root_path / request_data.uri

        if not p.exists():
            p.mkdir(parents=True)

        p = p / ('%s.json' % request_data.id)

        data = self._preapre_data(request_data)

        with p.open('w') as f:
            json.dump(data, f, indent=2)
