#!/usr/bin/env python3

from confluent_kafka import Producer
import json
import time

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class KafkaSettings(BaseSettings):
    bootstrap_servers: str = Field(serialization_alias="bootstrap.servers", default='localhost:9092')
    compression_type: str =  Field(serialization_alias="compression.type", default="none")

    model_config = SettingsConfigDict(env_prefix='KAFKA_')

settings = KafkaSettings()

producer = Producer(settings.model_dump(by_alias=True))

with open('system_snapshot.json', 'r') as f:
    message = f.read()

# Send message
topic = "test-topic"
producer.produce(topic, message)

# Wait for message delivery
producer.flush()

print(f"Message sent to topic '{topic}': {message}")
