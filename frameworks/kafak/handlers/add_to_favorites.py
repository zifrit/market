from frameworks.kafak.handlers.base import AbstractHandler
from frameworks.ch_tables import AddToFavorites


class AddToFavoritesHandler(AbstractHandler):

    def processing(self, x: str, y: AddToFavorites):
        return x + y.to_kafka()
