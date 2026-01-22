#!/usr/bin/env python3

from confluent_kafka import Producer
import time
import argparse
import random

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class KafkaSettings(BaseSettings):
    bootstrap_servers: str = Field(serialization_alias="bootstrap.servers", default='localhost:9092')
    compression_type: str = Field(serialization_alias="compression.type", default="none")

    model_config = SettingsConfigDict(env_prefix='KAFKA_')

ALL_COMPRESSION_TYPES = ["zstd", "none", "gzip", "lz4", "snappy"]

def produce(producer, topic, message):
    while True:
        try:
            producer.produce(topic, message)
            break
        except BufferError:
            producer.poll(0)
            time.sleep(0.0)

def main():
    parser = argparse.ArgumentParser(description='Test Kafka compression types')
    parser.add_argument('--compression', '-c', type=str, choices=ALL_COMPRESSION_TYPES + ['all'],
                        default='all', help='Compression type to test (default: all)')
    parser.add_argument('--files', '-n', type=int, default=2,
                        help='Number of JSON files to load (default: 2)')
    parser.add_argument('--messages', '-m', type=int, default=5000,
                        help='Number of messages to produce (default: 5000)')
    args = parser.parse_args()

    compression_types = ALL_COMPRESSION_TYPES if args.compression == 'all' else [args.compression]

    messages = []
    for i in range(1, args.files + 1):
        with open(f'system_snapshot_{i:02d}.json', 'r') as f:
            messages.append(f.read())

    for compression_type in compression_types:
        start = time.time_ns()
        print(f"Start compression_type {compression_type}")
        kafka_settings = KafkaSettings(compression_type=compression_type)

        producer = Producer(kafka_settings.model_dump(by_alias=True))
        topic = "json-compression1"
        for i in range(args.messages):
            produce(producer, topic, random.choice(messages))

        producer.flush()
        end = time.time_ns()
        duration_sec = (end - start) / 10**9
        print(f"End compression_type {compression_type} in time {duration_sec}s")

if __name__ == "__main__":
    main()
