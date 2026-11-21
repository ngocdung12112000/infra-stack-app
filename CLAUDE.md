# CLAUDE.md (stackshop-infra)

Phase 0: local third-party infra only (MySQL, MongoDB, Redis, Mailpit, Prometheus, Grafana). Kafka, RabbitMQ, ES, LocalStack come in later phases. `k8s/` is empty for now.

```bash
docker compose -f local/compose.yml up -d     # creates network "stackshop"
docker compose -f local/compose.yml config    # validate
```

Ports: mysql 3306, mongo 27017, redis 6379, mailpit 8025 (UI) / 1025 (SMTP), prometheus 9090, grafana 3030 (admin/admin).
