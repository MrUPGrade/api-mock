import json
from logging import getLogger
import falcon

from apimock.response import SimpleResponseProcessor

debug_log = getLogger('debugger')
log = getLogger()


class FolderBasedSink:
    def __init__(self, data_root):
        self._data_root = data_root

    def __call__(self, req, resp):
        log.info('Processing request: %s', req.relative_uri)

        uri = req.relative_uri.rstrip(req.query_string).rstrip('?').lstrip('/')
        debug_log.debug('URI: %s', uri or '/')

        if uri:
            path = self._data_root / uri
        else:
            path = self._data_root
            debug_log.debug('PATH: %s', path)

        file_name = req.method.lower() + '.json'
        debug_log.debug('FILE_NAME: %s', file_name)

        if not path.exists():
            raise falcon.HTTPNotFound()

        file_path = path / file_name
        debug_log.debug('FILE_PATH: %s', file_path)

        if not file_path.is_file():
            file_list = []
            for file in file_path.parent.glob('*.json'):
                file = str(file.parts[-1]).rstrip('.json')
                file_list.append(file)

            if len(file_list) > 0:
                raise falcon.HTTPMethodNotAllowed(file_list)
            else:
                raise falcon.HTTPNotFound()

        with file_path.open() as f:
            data = json.load(f)

        response_data = data.get('response', dict())

        processor = SimpleResponseProcessor()
        processor.process_response(resp, response_data)
