from frameworks.kafak.handlers.base import AbstractHandler
from frameworks.ch_tables import ObjViews


class ObjViewsHandler(AbstractHandler):

    def processing(self, x: str, y: ObjViews):
        return x + y.to_kafka()
