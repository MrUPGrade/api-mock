import json
import falcon
import attr

from pathlib import Path
from logging import getLogger

from apimock.request import SimpleRequestLogger, RequestWrapper
from apimock.response import ResponseProcessorFactory

debug_log = getLogger('debug')
log = getLogger()


@attr.s
class FolderScaner:
    _data_root = attr.ib(validator=attr.validators.instance_of(Path))

    def scan_or_raise(self, uri, http_method):
        if uri:
            path = self._data_root / uri
        else:
            path = self._data_root
            debug_log.debug('PATH: %s', path)

        file_name = http_method + '.json'
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

        return data


@attr.s
class FolderBasedSink:
    _data_root = attr.ib()
    _output_root = attr.ib()

    def __call__(self, request, response):
        log.info('Processing request: %s', request.relative_uri)

        request_data = RequestWrapper.build(request)
        debug_log.debug('URI: %s', request_data.uri or '/')

        scaner = FolderScaner(self._data_root)
        data = scaner.scan_or_raise(request_data.uri, request_data.method)

        mock_response_data = data.get('response', dict())
        response_processor_name = data.get('response_type', 'simple')

        processor = ResponseProcessorFactory.build(response_processor_name)
        processor.process(response, mock_response_data)

        req_log = SimpleRequestLogger(self._output_root)
        req_log.process(request_data, mock_response_data)
