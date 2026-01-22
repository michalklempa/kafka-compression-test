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

## Results
### Message count: 200,000 (files: 100)

| Compression   | Time   | Log Size   |
|---------------|--------|------------|
| zstd          | 5.24s  | 121M       |
| none          | 4.17s  | 1.5G       |
| gzip          | 51.66s | 204M       |
| lz4           | 3.27s  | 381M       |
| snappy        | 4.38s  | 381M       |