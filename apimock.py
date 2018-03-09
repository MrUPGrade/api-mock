import json
import logging
import falcon

from pathlib import Path

logging.basicConfig(level=logging.DEBUG)

api = falcon.API()

mock_folder = Path(__file__).parent / 'mock_data'


class ApiSink:
    def __init__(self, data_root):
        self._data_root = data_root

    def __call__(self, req, resp):
        uri = req.relative_uri.lstrip('/')
        logging.debug('URI: %s', uri)

        if uri:
            path = self._data_root / uri
        else:
            path = self._data_root
        logging.debug('PATH: %s', path)

        file_name = req.method.lower() + '.json'
        logging.debug('FILE_NAME: %s', file_name)

        if not path.exists():
            raise falcon.HTTPNotFound()

        path = path / file_name

        if not path.is_file():
            file_list = []
            for file in path.parent.glob('*.json'):
                file = str(file.parts[-1]).rstrip('.json')
                file_list.append(file)

            if len(file_list) > 0:
                raise falcon.HTTPMethodNotAllowed(file_list)
            else:
                raise falcon.HTTPNotFound()

        with path.open() as f:
            data = json.load(f)

        resp.media = data['response']


sink = ApiSink(mock_folder)
api.add_sink(sink=sink, prefix='/')

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    server = make_server('0.0.0.0', 8000, api)
    server.serve_forever()
