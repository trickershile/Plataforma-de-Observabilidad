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
        """Must use a slim base image"""
        with open(self.dockerfile_path, "r") as f:
            content = f.read()
        self.assertIn("python:3.11-slim", content)

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

    def test_healthcheck_configured(self):
        """Must have HEALTHCHECK instruction"""
        with open(self.dockerfile_path, "r") as f:
            content = f.read()
        self.assertIn("HEALTHCHECK", content)

    def test_java_17_installed(self):
        """Must install Java 17 JRE for PySpark"""
        with open(self.dockerfile_path, "r") as f:
            content = f.read()
        self.assertIn("openjdk-17-jre-headless", content)


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
        """Must have livenessProbe on port 8501 with 3 failure threshold"""
        with open(self.deployment_path, "r") as f:
            content = f.read()
        self.assertIn("livenessProbe", content)
        self.assertIn("port: 8501", content)
        self.assertIn("failureThreshold: 3", content)

    def test_startup_probe_configured(self):
        """Must have startupProbe for slow-starting Spark apps"""
        with open(self.deployment_path, "r") as f:
            content = f.read()
        self.assertIn("startupProbe", content)
        self.assertIn("failureThreshold: 30", content)

    def test_readiness_probe_configured(self):
        """Must have readinessProbe"""
        with open(self.deployment_path, "r") as f:
            content = f.read()
        self.assertIn("readinessProbe", content)

    def test_service_defined(self):
        """Must have a Service manifest to expose the deployment"""
        with open(self.deployment_path, "r") as f:
            content = f.read()
        self.assertIn("kind: Service", content)
        self.assertIn("lakehouse-observabilidad-service", content)

    def test_observabilidad_namespace(self):
        """Must use observabilidad namespace instead of default"""
        with open(self.deployment_path, "r") as f:
            content = f.read()
        self.assertIn("namespace: observabilidad", content)

    def test_lakehouse_env_configured(self):
        """Must have LAKEHOUSE_PATH env var"""
        with open(self.deployment_path, "r") as f:
            content = f.read()
        self.assertIn("LAKEHOUSE_PATH", content)


class TestNamespaceYaml(unittest.TestCase):
    """Validate k8s namespace.yml configuration"""

    def setUp(self):
        self.namespace_path = os.path.join(
            os.path.dirname(__file__), "..", "k8s", "namespace.yml"
        )

    def test_namespace_exists(self):
        """namespace.yml must exist in k8s folder"""
        self.assertTrue(os.path.exists(self.namespace_path))

    def test_namespace_name(self):
        """Must define observabilidad namespace"""
        with open(self.namespace_path, "r") as f:
            content = f.read()
        self.assertIn("name: observabilidad", content)


class TestIstioTelemetry(unittest.TestCase):
    """Validate k8s istio-telemetry.yml configuration"""

    def setUp(self):
        self.istio_path = os.path.join(
            os.path.dirname(__file__), "..", "k8s", "istio-telemetry.yml"
        )

    def test_istio_exists(self):
        """istio-telemetry.yml must exist in k8s folder"""
        self.assertTrue(os.path.exists(self.istio_path))

    def test_telemetry_defined(self):
        """Must have Telemetry resource for Prometheus metrics"""
        with open(self.istio_path, "r") as f:
            content = f.read()
        self.assertIn("kind: Telemetry", content)
        self.assertIn("prometheus", content)

    def test_access_logging_configured(self):
        """Must have access logging with envoy"""
        with open(self.istio_path, "r") as f:
            content = f.read()
        self.assertIn("accessLogging", content)
        self.assertIn("envoy", content)

    def test_resolution_dns(self):
        """ServiceEntries must use DNS resolution, not STATIC"""
        with open(self.istio_path, "r") as f:
            content = f.read()
        self.assertIn("resolution: DNS", content)
        self.assertNotIn("resolution: STATIC", content)

    def test_observabilidad_namespace(self):
        """Must use observabilidad namespace"""
        with open(self.istio_path, "r") as f:
            content = f.read()
        self.assertIn("namespace: observabilidad", content)


class TestDockerIgnore(unittest.TestCase):
    """Validate .dockerignore configuration"""

    def setUp(self):
        self.dockerignore_path = os.path.join(
            os.path.dirname(__file__), "..", ".dockerignore"
        )

    def test_dockerignore_exists(self):
        """.dockerignore must exist at project root"""
        self.assertTrue(os.path.exists(self.dockerignore_path))

    def test_excludes_lakehouse_data(self):
        """Must exclude lakehouse data layers"""
        with open(self.dockerignore_path, "r") as f:
            content = f.read()
        self.assertIn("lakehouse/bronze/", content)
        self.assertIn("lakehouse/silver/", content)
        self.assertIn("lakehouse/gold/", content)

    def test_excludes_git(self):
        """Must exclude .git directory"""
        with open(self.dockerignore_path, "r") as f:
            content = f.read()
        self.assertIn(".git/", content)


class TestSonarProperties(unittest.TestCase):
    """Validate sonar-project.properties configuration"""

    def setUp(self):
        self.sonar_path = os.path.join(
            os.path.dirname(__file__), "..", "sonar-project.properties"
        )

    def test_sonar_exists(self):
        """sonar-project.properties must exist at project root"""
        self.assertTrue(os.path.exists(self.sonar_path))

    def test_no_placeholders(self):
        """Must not contain placeholder values"""
        with open(self.sonar_path, "r") as f:
            content = f.read()
        self.assertNotIn("tu_usuario", content)
        self.assertNotIn("tu_project_key", content)

    def test_sources_configured(self):
        """Must have sources configured for notebooks"""
        with open(self.sonar_path, "r") as f:
            content = f.read()
        self.assertIn("sonar.sources", content)
        self.assertIn("notebooks", content)


if __name__ == "__main__":
    unittest.main()
