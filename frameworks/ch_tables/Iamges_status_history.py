from datetime import datetime
from pydantic import BaseModel


class ImagesStatusHistory(BaseModel):
    status: str
    dt: datetime
    entity_id: int

    def to_kafka(self):
        return f"('{self.status}', '{self.dt.strftime('%Y-%m-%d %H:%M:%S')}', '{self.entity_id}'),"

    @staticmethod
    def topic_name():
        return "images_status_history"
