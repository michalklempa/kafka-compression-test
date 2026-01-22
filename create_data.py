#!/usr/bin/env python3
import json
import random
import string
import argparse
from datetime import datetime, timedelta

hostnames = [
    "kafka-test-server", "production-server-cluster-01.example.com",
    "web-server-us-east-1", "db-primary-replica-02.internal",
    "api-gateway-eu-west-1", "cache-node-03.prod", "worker-node-k8s-04",
    "monitoring-server-01", "log-aggregator-central", "build-agent-runner-05",
    "analytics-processor-07", "search-cluster-08", "message-queue-09",
    "storage-server-10", "backup-node-11", "cdn-edge-12"
]

cpu_models = [
    "Intel(R) Core(TM) i7-9700K CPU @ 3.60GHz",
    "AMD EPYC 7742 64-Core Processor @ 2.25GHz",
    "Intel(R) Xeon(R) Platinum 8275CL CPU @ 3.00GHz",
    "AMD Ryzen 9 5950X 16-Core Processor @ 3.40GHz",
    "Intel(R) Xeon(R) E5-2686 v4 @ 2.30GHz"
]

commands_templates = [
    ("/sbin/init", "/sbin/init splash", "root"),
    ("", "[kthreadd]", "root"),
    ("/usr/sbin/sshd", "/usr/sbin/sshd -D", "root"),
    ("/usr/lib/systemd/systemd-timesyncd", "/usr/lib/systemd/systemd-timesyncd", "systemd-timesync"),
    ("/usr/bin/containerd", "/usr/bin/containerd --config /etc/containerd/config.toml", "root"),
    ("/usr/bin/java", "/usr/bin/java -Xmx8G -Xms8G -server -XX:+UseG1GC -Dkafka.logs.dir=/opt/kafka/logs -cp /opt/kafka/libs/* kafka.Kafka /opt/kafka/config/kraft/server.properties", "root"),
    ("/usr/sbin/sshd", "sshd: admin@pts/0", "admin"),
    ("/bin/bash", "-bash --login", "admin"),
    ("/usr/bin/python3.11", "python3 /home/admin/applications/monitoring/system_monitor.py --daemon", "admin"),
    ("", "[migration/0]", "root"),
    ("", "[rcu_gp]", "root"),
    ("/usr/sbin/rsyslogd", "/usr/sbin/rsyslogd -n -iNONE", "root"),
    ("/usr/sbin/nginx", "/usr/sbin/nginx -g daemon off;", "root"),
    ("/usr/sbin/nginx", "nginx: worker process", "www-data"),
    ("/usr/sbin/mysqld", "/usr/sbin/mysqld --defaults-file=/etc/mysql/my.cnf --user=mysql --port=3306", "mysql"),
    ("/usr/bin/redis-server", "/usr/bin/redis-server /etc/redis/redis.conf", "redis"),
    ("/usr/share/elasticsearch/jdk/bin/java", "/usr/share/elasticsearch/jdk/bin/java -Xms4g -Xmx4g -Des.path.home=/usr/share/elasticsearch org.elasticsearch.bootstrap.Elasticsearch", "elastic"),
    ("/usr/bin/postgres", "/usr/bin/postgres -D /var/lib/postgresql/data", "postgres"),
    ("/usr/bin/node", "/usr/bin/node /home/node/app/server.js --port=3000", "node"),
    ("/usr/bin/dockerd", "/usr/bin/dockerd -H fd://", "root"),
    ("/usr/bin/kubelet", "/usr/bin/kubelet --config=/var/lib/kubelet/config.yaml", "root"),
    ("/usr/bin/prometheus", "/usr/bin/prometheus --config.file=/etc/prometheus/prometheus.yml", "prometheus"),
    ("", "[kworker/0:0-events]", "root"),
    ("", "[ksoftirqd/0]", "root"),
    ("/usr/bin/memcached", "/usr/bin/memcached -m 1024 -p 11211 -u memcache", "memcache"),
]

def random_hash():
    return ''.join(random.choices(string.hexdigits.lower(), k=40))

def random_time():
    return f"{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"

def random_start():
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"]
    if random.random() > 0.3:
        return f"{random.choice(months)}{random.randint(1,28):02d}"
    return f"{random.randint(0,23):02d}:{random.randint(0,59):02d}"

def generate_process(pid, ppid=1):
    full_path, cmd, user = random.choice(commands_templates)
    is_kernel = cmd.startswith("[")
    return {
        "pid": pid,
        "ppid": ppid,
        "user": user,
        "command": cmd,
        "full_path": full_path,
        "file_hash": "" if is_kernel else random_hash(),
        "cpu_percent": 0.0 if is_kernel else round(random.uniform(0, 50), 1),
        "memory_percent": 0.0 if is_kernel else round(random.uniform(0.1, 30), 1),
        "vsz_kb": 0 if is_kernel else random.randint(10000, 16000000),
        "rss_kb": 0 if is_kernel else random.randint(1024, 8000000),
        "tty": "?" if is_kernel or random.random() < 0.7 else f"pts/{random.randint(0,5)}",
        "stat": random.choice(["S", "Ss", "Ssl", "S+", "Sl", "R"]),
        "start_time": random_start(),
        "time": random_time()
    }

def generate_snapshot(index):
    base = datetime(2025, 8, 1) + timedelta(hours=index*6, minutes=random.randint(0,59))
    cores = random.choice([4, 8, 16, 32, 64])
    total_mem = random.choice([8192, 16384, 32768, 65536, 131072])
    used_mem = random.randint(int(total_mem*0.2), int(total_mem*0.9))
    total_disk = random.choice([256, 512, 1024, 2048, 4096])
    used_disk = random.randint(int(total_disk*0.1), int(total_disk*0.85))

    procs = [
        {"pid": 1, "ppid": 0, "user": "root", "command": "/sbin/init splash", "full_path": "/sbin/init", "file_hash": random_hash(), "cpu_percent": 0.0, "memory_percent": 0.1, "vsz_kb": 225280, "rss_kb": 9216, "tty": "?", "stat": "Ss", "start_time": random_start(), "time": "00:00:45"},
        {"pid": 2, "ppid": 0, "user": "root", "command": "[kthreadd]", "full_path": "", "file_hash": "", "cpu_percent": 0.0, "memory_percent": 0.0, "vsz_kb": 0, "rss_kb": 0, "tty": "?", "stat": "S", "start_time": random_start(), "time": "00:00:00"}
    ]
    used_pids = {1, 2}
    for _ in range(random.randint(10, 20)):
        pid = random.randint(100, 65535)
        while pid in used_pids:
            pid = random.randint(100, 65535)
        used_pids.add(pid)
        parent_candidates = [1, 2] + [p["pid"] for p in procs[2:]][:3]
        procs.append(generate_process(pid, random.choice(parent_candidates) if len(procs) > 2 else 1))
    procs.sort(key=lambda x: x["pid"])

    return {
        "timestamp": base.strftime("%Y-%m-%dT%H:%M:%S.") + f"{random.randint(0,999):03d}Z",
        "hostname": random.choice(hostnames),
        "system_info": {
            "uptime": random.randint(3600, 10000000),
            "load_average": [round(random.uniform(0.1, 5), 2), round(random.uniform(0.1, 4), 2), round(random.uniform(0.1, 3), 2)],
            "cpu": {
                "model": random.choice(cpu_models),
                "cores": cores,
                "threads": cores * random.choice([1, 2]),
                "usage_percent": round(random.uniform(5, 95), 1)
            },
            "memory": {
                "total_mb": total_mem,
                "used_mb": used_mem,
                "free_mb": total_mem - used_mem,
                "usage_percent": round(used_mem / total_mem * 100, 1)
            },
            "disk": {
                "total_gb": total_disk,
                "used_gb": used_disk,
                "free_gb": total_disk - used_disk,
                "usage_percent": round(used_disk / total_disk * 100, 1)
            }
        },
        "processes": procs
    }

def main():
    parser = argparse.ArgumentParser(description='Generate system snapshot JSON files')
    parser.add_argument('--start', type=int, default=3, help='Starting file number (default: 3)')
    parser.add_argument('--count', type=int, default=98, help='Number of files to generate (default: 98)')
    args = parser.parse_args()

    for i in range(args.start, args.start + args.count):
        snapshot = generate_snapshot(i)
        filename = f"system_snapshot_{i:02d}.json"
        with open(filename, 'w') as f:
            json.dump(snapshot, f, indent=2)
        print(f"Created {filename}")

    print(f"Done! Created {args.count} JSON files ({args.start:02d}-{args.start + args.count - 1:02d})")

if __name__ == "__main__":
    main()
