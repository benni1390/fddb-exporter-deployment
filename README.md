# fddb-exporter (Helm chart)

Compact Helm chart for the FDDB Prometheus exporter.

Helm repository: https://benni1390.github.io/fddb-exporter-deployment/

## Quick start

- Add the Helm repo:

  ```bash
  helm repo add benni1390 https://benni1390.github.io/fddb-exporter-deployment
  helm repo update
  ```

- Install the chart:

  ```bash
  helm install fddb-exporter benni1390/fddb-exporter \
    --namespace monitoring --create-namespace \
    --version 0.1.0 \
    --set image.repository=ghcr.io/benni1390/fddb-exporter,image.tag=sha-<sha>
  ```

- Show chart values:

  ```bash
  helm show values benni1390/fddb-exporter --version 0.1.0
  ```

## Repository layout (recommended)

For multiple charts use a `charts/` directory with one folder per chart:

```
charts/
  fddb-exporter/
  another-chart/
.github/
README.md
```

Current chart sources: `chart/fddb-exporter`. Move to `charts/` if you plan multiple charts.

## Notes

- CI packages the chart and publishes it as a Helm repo via GitHub Pages (branch `gh-pages`).
- Use a Personal Access Token (PAT) stored in repo secrets for publishing (e.g. `CR_PAT`).
- Do not commit credentials or tokens to the repository.

## Troubleshooting

- 404 on `https://benni1390.github.io/fddb-exporter-deployment/` → the `index.yaml` must exist in the `gh-pages` branch; CI generates it on release.
- Image pull errors from ghcr.io → check whether the image is public or supply ImagePullSecrets.

## Migration (optional)

Move chart to `charts/` while keeping Git history:

```bash
# from repo root
mkdir -p charts
git mv chart/fddb-exporter charts/
# remove empty 'chart' dir if present
rmdir chart || true
git add .
git commit -m "chore: move helm chart to charts/ for multi-chart layout"
```

See `chart/fddb-exporter/values.yaml` and `secret.yaml.example` for configurable options.
