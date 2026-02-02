# fddb-exporter-deployment

This repository contains the Helm chart for the FDDB Prometheus Exporter.

## Quick start

```bash
# install with Helm (creates namespace if missing)
helm repo add local-file "$(pwd)/chart" || true
helm install fddb-exporter ./chart/fddb-exporter --namespace monitoring --create-namespace

# or package and install
helm package chart/fddb-exporter
helm install fddb-exporter ./fddb-exporter-0.1.0.tgz --namespace monitoring --create-namespace
```

## Values

See `chart/fddb-exporter/values.yaml` for configurable options (image, resources, env, secrets).

## Image pull / Private GHCR

If your image is private, create an image pull secret before install:

```bash
kubectl create secret docker-registry ghcr-cred \
  --docker-server=ghcr.io \
  --docker-username=<github-username> \
  --docker-password=<PAT> \
  --docker-email=<email> \
  -n monitoring
```

Then set `imagePullSecrets` in `values.yaml` or with `--set`.

## Files

- `chart/fddb-exporter/` — Helm chart (templates + values)
- `secret.yaml.example` — example for required Kubernetes secrets

## License

MIT
