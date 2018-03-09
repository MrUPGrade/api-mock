import falcon
import os

from pathlib import Path

from apimock.sinks import FolderBasedSink


def bootstrap_api():
    api = falcon.API()

    mock_folder = Path(os.getcwd()) / 'mock'

    sink = FolderBasedSink(mock_folder)
    api.add_sink(sink=sink, prefix='/')

    return api
