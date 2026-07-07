import os
import unittest


class TestDockerfile(unittest.TestCase):
    """Validate Dockerfile configuration"""

    def setUp(self):
        self.dockerfile_path = os.path.join(
            os.path.dirname(__file__), "..", "Dockerfile"
        )

    def test_dockerfile_exists(self):
        """Dockerfile must exist at project root"""
        self.assertTrue(os.path.exists(self.dockerfile_path))

    def test_dockerfile_uses_slim_image(self):
        """Must use python:3.10-slim base image"""
        with open(self.dockerfile_path, "r") as f:
            content = f.read()
        self.assertIn("python:3.10-slim", content)

    def test_exposes_required_ports(self):
        """Must expose Streamlit (8501), Spark UI (4040) and Jupyter (8888)"""
        with open(self.dockerfile_path, "r") as f:
            content = f.read()
        self.assertIn("8501", content)
        self.assertIn("4040", content)
        self.assertIn("8888", content)

    def test_cmd_runs_orquestador(self):
        """Default CMD must execute orquestador_planta.py"""
        with open(self.dockerfile_path, "r") as f:
            content = f.read()
        self.assertIn("orquestador_planta.py", content)


class TestDeploymentYaml(unittest.TestCase):
    """Validate K8s deployment.yml configuration"""

    def setUp(self):
        self.deployment_path = os.path.join(
            os.path.dirname(__file__), "..", "k8s", "deployment.yml"
        )

    def test_deployment_exists(self):
        """deployment.yml must exist in k8s folder"""
        self.assertTrue(os.path.exists(self.deployment_path))

    def test_three_replicas(self):
        """Must configure exactly 3 replicas for high availability"""
        with open(self.deployment_path, "r") as f:
            content = f.read()
        self.assertIn("replicas: 3", content)

    def test_resource_limits_configured(self):
        """Must have CPU (1000m) and Memory (1Gi) limits"""
        with open(self.deployment_path, "r") as f:
            content = f.read()
        self.assertIn("cpu: \"1000m\"", content)
        self.assertIn("memory: \"1Gi\"", content)

    def test_liveness_probe_configured(self):
        """Must have livenessProbe on port 8501"""
        with open(self.deployment_path, "r") as f:
            content = f.read()
        self.assertIn("livenessProbe", content)
        self.assertIn("port: 8501", content)


if __name__ == "__main__":
    unittest.main()
