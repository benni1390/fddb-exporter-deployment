# fddb-exporter Helm Chart

Official Helm chart for deploying the FDDB Prometheus exporter to Kubernetes.

## Installation

### Add Helm Repository

```bash
helm repo add benni1390 https://benni1390.github.io/fddb-exporter-deployment
helm repo update
```

### Install Chart

```bash
helm install fddb-exporter benni1390/fddb-exporter \
  --namespace monitoring --create-namespace \
  --set env.FDDB_USERNAME=your-username \
  --set env.FDDB_PASSWORD=your-password
```

### Install with Specific Version

```bash
helm install fddb-exporter benni1390/fddb-exporter \
  --namespace monitoring --create-namespace \
  --version 0.0.13 \
  --set image.tag=0.1.0 \
  --set env.FDDB_USERNAME=your-username \
  --set env.FDDB_PASSWORD=your-password
```

### Upgrade Existing Installation

```bash
helm upgrade fddb-exporter benni1390/fddb-exporter \
  --namespace monitoring \
  --version 0.0.13 \
  --set image.tag=0.1.0
```

## Configuration

### View Available Values

```bash
helm show values benni1390/fddb-exporter --version 0.0.13
```

### Common Configuration Options

```yaml
# values.yaml
image:
  repository: ghcr.io/benni1390/fddb-exporter
  tag: "0.1.0"
  pullPolicy: IfNotPresent

env:
  FDDB_USERNAME: "your-username"
  FDDB_PASSWORD: "your-password"
  EXPORTER_PORT: "8000"
  SCRAPE_INTERVAL: "3600"

service:
  type: ClusterIP
  port: 8000

serviceMonitor:
  enabled: false
```

### Using Secrets

For production, use Kubernetes secrets instead of plain values:

```bash
# Create secret
kubectl create secret generic fddb-credentials \
  --namespace monitoring \
  --from-literal=username=your-username \
  --from-literal=password=your-password

# Reference in values
helm install fddb-exporter benni1390/fddb-exporter \
  --namespace monitoring \
  --set env.FDDB_USERNAME="" \
  --set env.FDDB_PASSWORD="" \
  --set existingSecret=fddb-credentials
```

See `secret.yaml.example` for more details.

## ServiceMonitor (Prometheus Operator)

Enable automatic Prometheus scraping:

```yaml
serviceMonitor:
  enabled: true
  interval: 5m
```

## Troubleshooting

### Image Pull Errors

If you get image pull errors from ghcr.io:
- Check if image is public
- Verify image tag exists: `docker pull ghcr.io/benni1390/fddb-exporter:0.1.0`
- Supply ImagePullSecrets if needed

### No Logs Visible

```bash
# Check pod status
kubectl get pods -n monitoring

# View logs
kubectl logs -n monitoring -l app=fddb-exporter -f

# Describe pod
kubectl describe pod -n monitoring -l app=fddb-exporter
```

### Metrics Not Available

```bash
# Port forward to test locally
kubectl port-forward -n monitoring svc/fddb-exporter 8000:8000

# Test metrics endpoint
curl http://localhost:8000/metrics
```

## Uninstall

```bash
helm uninstall fddb-exporter --namespace monitoring
```

---

## Development

### Repository Structure

```
fddb-exporter-deployment/
├── chart/
│   └── fddb-exporter/          # Helm chart sources
│       ├── Chart.yaml          # Chart metadata + version
│       ├── values.yaml         # Default configuration
│       ├── templates/          # Kubernetes manifests
│       │   ├── deployment.yaml
│       │   ├── service.yaml
│       │   └── servicemonitor.yaml
│       └── README.md
├── .github/
│   └── workflows/
│       ├── package-and-publish.yml  # Release workflow
│       └── test.yml                 # Test workflow
├── tests/
│   └── test_helm_release.py    # Helm chart tests
└── secret.yaml.example         # Example secret configuration
```

### Local Testing

```bash
# Lint chart
make lint

# Package chart
make package

# Run tests
make test
```

### Creating a Release

1. Update `chart/fddb-exporter/Chart.yaml` version (e.g., `0.0.14`)
2. Commit and push to main (or merge PR)
3. Workflow automatically:
   - Creates git tag `v0.0.14`
   - Packages Helm chart
   - Publishes to GitHub Pages
   - Creates GitHub release

### CI/CD Workflows

- **Test**: Runs on every PR - validates chart
- **Release**: Triggers on Chart.yaml version changes - publishes chart

### Helm Repository

Charts are published to GitHub Pages:
- URL: `https://benni1390.github.io/fddb-exporter-deployment`
- Branch: `gh-pages`
- Contains: `index.yaml`, `*.tgz` packages, `index.html`

### Multi-Chart Layout (Optional)

To support multiple charts, restructure to:

```
charts/
  fddb-exporter/
  another-chart/
```

Migration:

```bash
mkdir -p charts
git mv chart/fddb-exporter charts/
git commit -m "chore: move to multi-chart layout"
```

Update workflows to reference `charts/fddb-exporter`.

### Contributing

1. Create feature branch
2. Make changes to chart
3. Update tests if needed
4. Create PR to main

## License

See main repository `LICENSE` file.

