from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class ObjTypes(Enum):
    PRODUCT = "product"
    SHOP = "shop"
    HUMANIMAGES = "humanimages"


class ObjViews(BaseModel):
    obj: ObjTypes
    dt: datetime
    entity_id: int

    def to_kafka(self):
        return f"('{self.obj.value}', '{self.dt.strftime('%Y-%m-%d %H:%M:%S')}', '{self.entity_id}'),"

    @staticmethod
    def topic_name():
        return "obj_views"
