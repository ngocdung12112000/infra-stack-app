# CLAUDE.md (stackshop-infra)

Phase 0: local third-party infra only (MySQL, MongoDB, Redis, Mailpit, Prometheus, Grafana). Kafka, RabbitMQ, ES, LocalStack come in later phases. `k8s/apps/identity` is the first service (Kustomize base + dev/staging/prod overlays); ArgoCD Applications are in `argocd/apps/`.

```bash
docker compose -f local/compose.yml up -d     # creates network "stackshop"
docker compose -f local/compose.yml config    # validate
```

Ports: mysql 3306, mongo 27017, redis 6379, mailpit 8025 (UI) / 1025 (SMTP), prometheus 9090, grafana 3030 (admin/admin).

MongoDB runs as a single-node replica set `rs0` (needed for transactions). Connection strings:
- containers on the `stackshop` network: `mongodb://mongo:27017/?replicaSet=rs0`
- host tools (mongosh, Compass, `dotnet run` from the IDE): `mongodb://localhost:27017/?directConnection=true`

Monitoring: `monitoring/dashboards/*.json` are provisioned into local Grafana (folder StackShop). Alert rules are authored as PrometheusRule CRs in `monitoring/rules/`; the local Prometheus reads the generated copies in `monitoring/prometheus/rules/`:

```bash
python monitoring/scripts/render-local-rules.py   # regenerate after editing monitoring/rules/*.rules.yaml (CI runs --check)
curl -X POST localhost:9090/-/reload               # reload Prometheus (lifecycle API enabled)
```

K8s checks: `kubectl kustomize k8s/apps/<svc>/overlays/<env> | kubeconform -strict -ignore-missing-schemas -`, plus `kube-linter lint`.
Scrape targets for backend services (gateway, catalog, identity on :8080) are DOWN until those containers run.

