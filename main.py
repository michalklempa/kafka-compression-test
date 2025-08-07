#!/usr/bin/env python3

from confluent_kafka import Producer
import json
import time

from pydantic_settings import BaseSettings

class KafkaSettings(BaseSettings):
    bootstrap_servers: str = 'localhost:9092'
    compression_type: str = 'none'

    class Config:
        env_prefix = 'KAFKA_'
        case_sensitive = False

settings = KafkaSettings()

producer = Producer(settings.model_dump())

with open('system_snapshot.json', 'r') as f:
    message = f.read()

# Send message
topic = "test-topic"
producer.produce(topic, message)

# Wait for message delivery
producer.flush()

print(f"Message sent to topic '{topic}': {message}")
