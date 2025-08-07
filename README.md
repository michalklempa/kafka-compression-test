# Kafka Compression Test

Test Kafka producer with different compression algorithms using confluent-kafka Python library.

## Setup

```bash
docker-compose up -d
python main.py
```

## Configuration

- Bootstrap server: localhost:9092
- Topic: test-topic
- Compression: configurable (none, gzip, snappy, lz4, zstd)