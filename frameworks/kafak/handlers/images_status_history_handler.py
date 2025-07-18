from frameworks.kafak.handlers.base import AbstractHandler
from frameworks.ch_tables import ImagesStatusHistory


class ImagesStatusHistoryHandler(AbstractHandler):

    def processing(self, x: str, y: ImagesStatusHistory):
        return x + y.to_kafka()
