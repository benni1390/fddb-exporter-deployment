import yaml
import os
import subprocess
from pathlib import Path
import shutil
import pytest

CHART_PATH = "chart/fddb-exporter"
CHART_YAML = f"{CHART_PATH}/Chart.yaml"


def docker_available():
    """Check if docker command is available"""
    return shutil.which('docker') is not None


def test_chart_yaml_exists():
    """Chart.yaml must exist"""
    assert os.path.exists(CHART_YAML)


def test_chart_yaml_valid():
    """Chart.yaml must be valid YAML"""
    with open(CHART_YAML, 'r') as f:
        chart = yaml.safe_load(f)
    assert chart is not None
    assert 'apiVersion' in chart
    assert 'name' in chart
    assert 'version' in chart


def test_chart_has_required_fields():
    """Chart.yaml must have all required fields"""
    with open(CHART_YAML, 'r') as f:
        chart = yaml.safe_load(f)

    required_fields = ['apiVersion', 'name', 'description', 'type', 'version', 'appVersion']
    for field in required_fields:
        assert field in chart, f"Missing required field: {field}"


def test_chart_version_format():
    """Chart version must follow semver format"""
    with open(CHART_YAML, 'r') as f:
        chart = yaml.safe_load(f)

    version = chart['version']
    parts = version.split('.')
    assert len(parts) == 3, "Version must be in format X.Y.Z"
    assert all(part.isdigit() for part in parts), "Version parts must be numeric"


def test_helm_lint():
    """Helm lint must pass"""
    if not docker_available():
        pytest.skip("Docker not available")

    result = subprocess.run(
        ['docker', 'run', '--rm', '-v', f'{os.getcwd()}:/workspace', '-w', '/workspace',
         'alpine/helm:latest', 'lint', CHART_PATH],
        capture_output=True,
        text=True,
        timeout=30
    )
    assert result.returncode == 0, f"Helm lint failed: {result.stderr}"


def test_helm_template_renders():
    """Helm template must render without errors"""
    if not docker_available():
        pytest.skip("Docker not available")

    result = subprocess.run(
        ['docker', 'run', '--rm', '-v', f'{os.getcwd()}:/workspace', '-w', '/workspace',
         'alpine/helm:latest', 'template', 'test-release', CHART_PATH],
        capture_output=True,
        text=True,
        timeout=30
    )
    assert result.returncode == 0, f"Helm template failed: {result.stderr}"
    assert len(result.stdout) > 0, "Helm template produced no output"


def test_chart_package():
    """Chart must be packageable"""
    if not docker_available():
        pytest.skip("Docker not available")

    output_dir = "/tmp/helm-test"
    os.makedirs(output_dir, exist_ok=True)

    result = subprocess.run(
        ['docker', 'run', '--rm', '-v', f'{os.getcwd()}:/workspace',
         '-v', f'{output_dir}:/output', '-w', '/workspace',
         'alpine/helm:latest', 'package', CHART_PATH, '-d', '/output'],
        capture_output=True,
        text=True,
        timeout=30
    )
    assert result.returncode == 0, f"Helm package failed: {result.stderr}"

    with open(CHART_YAML, 'r') as f:
        chart = yaml.safe_load(f)
    expected_package = f"{output_dir}/{chart['name']}-{chart['version']}.tgz"
    assert os.path.exists(expected_package), f"Package file not created: {expected_package}"

    os.remove(expected_package)


def test_workflow_file_exists():
    """Release workflow must exist"""
    workflow_path = ".github/workflows/package-and-publish.yml"
    assert os.path.exists(workflow_path)


def test_workflow_file_valid_yaml():
    """Release workflow must be valid YAML"""
    workflow_path = ".github/workflows/package-and-publish.yml"
    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)
    assert workflow is not None
    assert 'name' in workflow
    assert 'jobs' in workflow
    assert 'release' in workflow['jobs']


def test_workflow_triggers_on_chart_change():
    """Workflow must trigger on Chart.yaml changes"""
    workflow_path = ".github/workflows/package-and-publish.yml"
    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)

    # 'on' is a reserved keyword in YAML, parsed as True
    trigger = workflow.get('on') or workflow.get(True)
    assert trigger is not None, "Workflow must have trigger definition"
    assert 'push' in trigger
    assert 'paths' in trigger['push']
    assert 'chart/fddb-exporter/Chart.yaml' in trigger['push']['paths']


def test_workflow_creates_release():
    """Workflow must create GitHub release"""
    workflow_path = ".github/workflows/package-and-publish.yml"
    with open(workflow_path, 'r') as f:
        content = f.read()

    assert 'action-gh-release' in content or 'create-release' in content
    assert 'git tag' in content or 'tag_name' in content
