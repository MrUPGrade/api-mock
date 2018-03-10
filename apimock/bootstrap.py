import os
import logging
import falcon
import attr

from pathlib import Path
from wsgiref.simple_server import make_server

from apimock.sinks import FolderBasedSink

debug_log = logging.getLogger('debug')


@attr.s
class Config:
    log_level = attr.ib()
    debug = attr.ib()
    mock_dir = attr.ib()
    output_dir = attr.ib()

    def load_from_env(self):
        self.log_level = os.getenv('APIMOCK_LOG_LEVEL', self.log_level)
        self.debug = os.getenv('APIMOCK_DEBUG', self.debug)
        self.mock_dir = os.getenv('APIMOCK_MOCK_DIR', self.mock_dir)


def setup_logger(cfg):
    root_log_level = getattr(logging, cfg.log_level.upper())

    logging.basicConfig(level=root_log_level)

    if cfg.debug:
        debug_log = logging.getLogger('debug')
        debug_log.setLevel(logging.DEBUG)


def bootstrap_api(cfg):
    api = falcon.API()

    mock_folder = Path(cfg.mock_dir)

    if not mock_folder.is_absolute():
        mock_folder = Path(os.getcwd()) / mock_folder

    output_folder = Path(cfg.output_dir)

    if not output_folder.is_absolute():
        output_folder = Path(os.getcwd()) / output_folder

    debug_log.debug('MOCK_PATH: %s', mock_folder)

    sink = FolderBasedSink(mock_folder, output_folder)
    api.add_sink(sink=sink, prefix='/')

    return api


def run_app(config):
    cfg = Config(**config)
    cfg.load_from_env()

    setup_logger(cfg)

    app = bootstrap_api(cfg)

    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
