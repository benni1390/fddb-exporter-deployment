Helm chart for FDDB Prometheus exporter

Usage:

```bash
# install from local chart folder
helm install fddb-exporter ./chart/fddb-exporter --namespace monitoring --create-namespace
```

See `values.yaml` for configurable options (image, resources, env, secrets).
