import json
import attr

from datetime import datetime
from logging import getLogger

debug_log = getLogger('debug')


@attr.s
class RequestWrapper:
    uri = attr.ib(init=False)
    method = attr.ib(init=False)
    headers = attr.ib(init=False, default=attr.Factory(dict))
    _dt = attr.ib(init=False, default=attr.Factory(datetime.now))
    _req = attr.ib()

    @classmethod
    def build(cls, request):
        r = cls(request)
        r.uri = request.relative_uri.rstrip(request.query_string).rstrip('?').lstrip('/')
        r.method = request.method.lower()
        r.headers = dict(request.headers)
        return r

    @property
    def id(self):
        return '%s_%s' % (self.method, self._dt.strftime('%Y%m%d_%H%M%S_%f'))

    def _filter(self, attr, value):
        if attr.name in ('_dt', '_req'):
            return False

        return True

    def to_dict(self):
        return attr.asdict(self, filter=self._filter)


class SimpleRequestLogger:
    def __init__(self, root_path):
        self.root_path = root_path

    def _preapre_data(self, request_data, response_data):
        data = {}
        data['request'] = request_data.to_dict()
        data['response'] = response_data

        return data

    def _write_to_file(self, file, data):
        with file.open('w') as f:
            json.dump(data, f, indent=2)

    def process(self, request_data, response_data):
        path = self.root_path / request_data.uri

        if not path.exists():
            path.mkdir(parents=True)

        path = path / ('%s.json' % request_data.id)

        data = self._preapre_data(request_data, response_data)

        self._write_to_file(path, data)
