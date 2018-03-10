import json
import falcon
import attr

from logging import getLogger

from apimock.request import RequestParser, SimpleRequestLogger
from apimock.response import ResponseProcessorFactory

debug_log = getLogger('debug')
log = getLogger()


@attr.s
class FolderBasedSink:
    _data_root = attr.ib()
    _output_root = attr.ib()

    def __call__(self, request, response):
        log.info('Processing request: %s', request.relative_uri)

        request_parser = RequestParser()
        request_data = request_parser.process(request)

        if request_data.uri:
            path = self._data_root / request_data.uri
        else:
            path = self._data_root
            debug_log.debug('PATH: %s', path)

        file_name = request_data.method + '.json'
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

        request_logger = SimpleRequestLogger(self._output_root)
        request_logger.process(request_data, request)

        mock_response_data = data.get('response', dict())
        response_processor_name = data.get('response_type', 'simple')

        processor = ResponseProcessorFactory.build(response_processor_name)
        processor.process(response, mock_response_data)
