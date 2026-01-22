#!/usr/bin/env python3

from confluent_kafka import Consumer

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class KafkaSettings(BaseSettings):
    bootstrap_servers: str = Field(serialization_alias="bootstrap.servers", default='localhost:9092')
    group_id: str = Field(serialization_alias="group.id", default="test-consumer-group")
    auto_offset_reset: str = Field(serialization_alias="auto.offset.reset", default="earliest")

    model_config = SettingsConfigDict(env_prefix='KAFKA_')


kafka_settings = KafkaSettings()

consumer = Consumer(kafka_settings.model_dump(by_alias=True))

topic = f"json-compression1"
consumer.subscribe([topic])

try:
    while True:
        msg = consumer.poll(1.0)
        
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        print(msg.value())
        # print(f"Received message: {len(msg.value())} bytes from topic {msg.topic()} partition {msg.partition()} offset {msg.offset()}")

except KeyboardInterrupt:
    pass
finally:
    consumer.close()