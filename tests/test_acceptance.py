import os
import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "notebooks"))


class TestAcceptancePreDeploy(unittest.TestCase):
    """Pruebas de aceptación que deben pasar antes del despliegue en producción (IE13)"""

    def test_dockerfile_has_healthcheck(self):
        """Acceptance: Dockerfile must define HEALTHCHECK for container orchestration"""
        dockerfile_path = os.path.join(
            os.path.dirname(__file__), "..", "Dockerfile"
        )
        with open(dockerfile_path, "r") as f:
            content = f.read()
        self.assertIn("HEALTHCHECK", content)

    def test_k8s_has_startup_probe(self):
        """Acceptance: K8s deployment must have startupProbe for Spark slow start"""
        deployment_path = os.path.join(
            os.path.dirname(__file__), "..", "k8s", "deployment.yml"
        )
        with open(deployment_path, "r") as f:
            content = f.read()
        self.assertIn("startupProbe", content)
        self.assertIn("failureThreshold: 30", content)

    def test_k8s_has_resource_limits(self):
        """Acceptance: K8s deployment must have CPU and memory limits"""
        deployment_path = os.path.join(
            os.path.dirname(__file__), "..", "k8s", "deployment.yml"
        )
        with open(deployment_path, "r") as f:
            content = f.read()
        self.assertIn("cpu:", content)
        self.assertIn("memory:", content)

    def test_k8s_three_replicas(self):
        """Acceptance: K8s deployment must have 3 replicas for HA"""
        deployment_path = os.path.join(
            os.path.dirname(__file__), "..", "k8s", "deployment.yml"
        )
        with open(deployment_path, "r") as f:
            content = f.read()
        self.assertIn("replicas: 3", content)

    def test_k8s_has_service(self):
        """Acceptance: K8s must define a Service to expose the deployment"""
        deployment_path = os.path.join(
            os.path.dirname(__file__), "..", "k8s", "deployment.yml"
        )
        with open(deployment_path, "r") as f:
            content = f.read()
        self.assertIn("kind: Service", content)

    def test_istio_uses_dns_resolution(self):
        """Acceptance: Istio ServiceEntries must use DNS resolution"""
        istio_path = os.path.join(
            os.path.dirname(__file__), "..", "k8s", "istio-telemetry.yml"
        )
        with open(istio_path, "r") as f:
            content = f.read()
        self.assertIn("resolution: DNS", content)

    def test_cicd_triggers_on_push_develop(self):
        """Acceptance: CI/CD must trigger on push to develop"""
        cicd_path = os.path.join(
            os.path.dirname(__file__), "..", ".github", "workflows", "ci-cd.yml"
        )
        with open(cicd_path, "r") as f:
            content = f.read()
        self.assertIn('branches: ["develop", "main"]', content)

    def test_cicd_has_snyk_test(self):
        """Acceptance: CI/CD must fail on Snyk vulnerabilities (test, not monitor)"""
        cicd_path = os.path.join(
            os.path.dirname(__file__), "..", ".github", "workflows", "ci-cd.yml"
        )
        with open(cicd_path, "r") as f:
            content = f.read()
        self.assertIn("command: test", content)

    def test_sonarqube_waits_for_quality_gate(self):
        """Acceptance: SonarQube must block pipeline if quality gate fails"""
        cicd_path = os.path.join(
            os.path.dirname(__file__), "..", ".github", "workflows", "ci-cd.yml"
        )
        with open(cicd_path, "r") as f:
            content = f.read()
        self.assertIn("sonar.qualitygate.wait=true", content)

    def test_dependabot_configured(self):
        """Acceptance: Dependabot must be configured for pip and GitHub Actions"""
        dependabot_path = os.path.join(
            os.path.dirname(__file__), "..", ".github", "dependabot.yml"
        )
        self.assertTrue(os.path.exists(dependabot_path))
        with open(dependabot_path, "r") as f:
            content = f.read()
        self.assertIn("pip", content)
        self.assertIn("github-actions", content)

    def test_dockerignore_exists(self):
        """Acceptance: .dockerignore must exist to optimize builds"""
        dockerignore_path = os.path.join(
            os.path.dirname(__file__), "..", ".dockerignore"
        )
        self.assertTrue(os.path.exists(dockerignore_path))

    def test_k8s_namespace_not_default(self):
        """Acceptance: K8s resources must use observabilidad namespace, not default"""
        deployment_path = os.path.join(
            os.path.dirname(__file__), "..", "k8s", "deployment.yml"
        )
        with open(deployment_path, "r") as f:
            content = f.read()
        self.assertIn("namespace: observabilidad", content)
        self.assertNotIn("namespace: default", content)


if __name__ == "__main__":
    unittest.main()
