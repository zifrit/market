from typing import List

from kafka import KafkaProducer
from django.conf import settings
from pydantic import BaseModel

from frameworks.ch_tables.tables import Tables
from frameworks.kafak.handlers.handles import Handlers
from frameworks.utils import batch_iterator


class KafkaContextProducer:
    def __enter__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_NODES,
            value_serializer=lambda v: v.encode("utf-8"),
            linger_ms=10 * 5,
        )
        return self.producer

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.producer.flush()
        self.producer.close()


class KafkaLogSender(Handlers):

    @classmethod
    def save_table_data(cls, data: List[BaseModel], table: Tables):
        """Отправка данных в Kafka"""
        table_handler = cls.handlers.get(table)
        if settings.DEBUG:
            print(
                f"WRITING TO KAFKA -> Topic: {table.value} Value: {table_handler.convertor_func(data)}"
            )
            return
        with KafkaContextProducer() as kafka_producer:
            for batch in batch_iterator(data, 20):
                kafka_producer.send(table.value, table_handler.convertor_func(batch))
