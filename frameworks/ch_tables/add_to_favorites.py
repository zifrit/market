from datetime import datetime
from pydantic import BaseModel


class AddToFavorites(BaseModel):
    dt: datetime
    entity_id: int

    def to_kafka(self):
        return f"('{self.dt.strftime('%Y-%m-%d %H:%M:%S')}', '{self.entity_id}'),"

    @staticmethod
    def topic_name():
        return "add_to_favorites"
