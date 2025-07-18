import enum

from frameworks.ch_tables import ProductStatusHistory, ImagesStatusHistory, ObjViews


class Tables(enum.Enum):
    PRODUCT_STATUS_HISTORY = ProductStatusHistory.topic_name()
    IMAGES_STATUS_HISTORY = ImagesStatusHistory.topic_name()
    OBJ_VIEWS = ObjViews.topic_name()
