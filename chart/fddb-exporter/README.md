Helm chart for FDDB Prometheus Exporter

Usage:

```bash
helm install fddb-exporter ./chart/fddb-exporter --namespace monitoring --create-namespace
```

Values: see `values.yaml` for configurable options (image, resources, env, secrets).
