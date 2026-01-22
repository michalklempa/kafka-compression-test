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
### Message count: 20 000

| Time      | Compression | Log Size  |
|-----------|-------------|-----------|
| 0.9s      | none        | 303 MB    |
| 5s        | gzip        | 8.3 MB    |
| 0.6s      | snappy      | 34 MB     |
| 0.7s      | lz4         | 25 MB     |
| 0.7s      | zstd        | 1.3 MB    |

## Message count: 200_000

| Time  | Compression | Log Size |
|-------|-------------|----------|
| 7s    | none        | 3000 MB  |
| 54.7s | gzip        | 42 MB    |
| 3.7s  | snappy      | 340 MB   |
| 2.9s  | lz4         | 250 MB   |
| 3.8s  | zstd        | 13 MB    |

### Message count: 2 million

| Time      | Compression | Log Size  |
|-----------|-------------|-----------|
| 27.5s     | none        | 14 771 MB |
| 300s      | gzip        | 210 MB    |
| 16.4s     | snappy      | 1674 MB   |
| 12s       | lz4         | 1222 MB   |
| 10.3s     | zstd        | 61 MB     |

