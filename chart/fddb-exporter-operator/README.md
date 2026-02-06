# FDDB Exporter Operator Helm Chart

Kubernetes operator for automated deployment and management of fddb-exporter instances.

## Installation

### Add Helm Repository

```bash
helm repo add benni1390 https://benni1390.github.io/fddb-exporter-operator
helm repo update
```

### Install Operator

```bash
kubectl create namespace fddb-operator-system
helm install fddb-operator benni1390/fddb-exporter-operator \
  --namespace fddb-operator-system
```

### Install CRD

```bash
kubectl apply -f https://raw.githubusercontent.com/benni1390/fddb-exporter-operator/main/deploy/crds/fddbexporter_crd.yaml
```

## Usage

After installing the operator, create FddbExporter custom resources:

```yaml
apiVersion: fddb.benni1390.github.io/v1alpha1
kind: FddbExporter
metadata:
  name: my-fddb-exporter
  namespace: default
spec:
  helmChart:
    version: "0.0.14"
  image:
    tag: "0.0.1"
  scrapeInterval: "300"
  credentialsSecretName: fddb-credentials
```

## Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of operator replicas | `1` |
| `image.repository` | Operator image repository | `ghcr.io/benni1390/fddb-exporter-operator` |
| `image.tag` | Operator image tag | `latest` |
| `image.pullPolicy` | Image pull policy | `Always` |
| `resources.requests.cpu` | CPU request | `50m` |
| `resources.requests.memory` | Memory request | `128Mi` |
| `resources.limits.cpu` | CPU limit | `200m` |
| `resources.limits.memory` | Memory limit | `256Mi` |
