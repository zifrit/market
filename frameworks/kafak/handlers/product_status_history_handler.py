from frameworks.kafak.handlers.base import AbstractHandler
from frameworks.ch_tables import ProductStatusHistory


class ProductStatusHistoryHandler(AbstractHandler):

    def processing(self, x: str, y: ProductStatusHistory):
        return x + y.to_kafka()
