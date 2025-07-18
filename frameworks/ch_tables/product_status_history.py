import enum
from datetime import datetime
from pydantic import BaseModel


class ProductStatusHistory(BaseModel):
    status: str
    dt: datetime
    entity_id: int
    user_id: int

    def to_kafka(self):
        return f"('{self.status}', '{self.dt.strftime('%Y-%m-%d %H:%M:%S')}', '{self.entity_id}', '{self.user_id}'),"

    @staticmethod
    def topic_name():
        return "product_status_history"
