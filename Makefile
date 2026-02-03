.PHONY: lint package test-workflow test

lint:
	docker run --rm -v $(CURDIR):/workspace -w /workspace alpine/helm:latest lint chart/fddb-exporter

package:
	docker run --rm -v $(CURDIR):/workspace -w /workspace alpine/helm:latest package chart/fddb-exporter -d .charts

test-workflow:
	@echo "Testing workflow configuration..."
	docker run --rm -v $(CURDIR):/workspace -w /workspace alpine/helm:latest lint chart/fddb-exporter
	@echo "Workflow test passed"

test:
	docker run --rm -v $(CURDIR):/workspace -v /var/run/docker.sock:/var/run/docker.sock -w /workspace -e PYTHONPATH=/workspace python:3.11-slim \
		bash -c "pip install -r requirements.txt && pytest -v"
