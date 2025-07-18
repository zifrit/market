from collections.abc import Mapping

from frameworks.ch_tables.tables import Tables
from frameworks.kafak.handlers import (
    ProductStatusHistoryHandler,
    ImagesStatusHistoryHandler,
    ObjViewsHandler,
)
from frameworks.kafak.handlers.base import AbstractHandler


class Handlers:
    handlers: Mapping[Tables, AbstractHandler] = {
        Tables.PRODUCT_STATUS_HISTORY: ProductStatusHistoryHandler(),
        Tables.IMAGES_STATUS_HISTORY: ImagesStatusHistoryHandler(),
        Tables.OBJ_VIEWS: ObjViewsHandler(),
    }
