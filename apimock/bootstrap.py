import logging

import falcon
import os

from pathlib import Path

from apimock.sinks import FolderBasedSink


def setup_logger():
    logging.basicConfig(level=logging.DEBUG)

    debugger = logging.getLogger('debugger')
    debugger.setLevel(logging.DEBUG)


def bootstrap_api():
    api = falcon.API()

    mock_folder = Path(os.getcwd()) / 'mock'

    sink = FolderBasedSink(mock_folder)
    api.add_sink(sink=sink, prefix='/')

    return api
