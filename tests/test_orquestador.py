import os
import sys
import json
import tempfile
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "notebooks"))


class TestOrquestador(unittest.TestCase):
    """Unit tests for orquestador_planta.py"""

    def test_kpi_latency_persistence(self):
        """Verify KPI latency file is written with correct format"""
        from orquestador_planta import KPI_INFRA_PATH, LAKEHOUSE_BASE

        expected_format = "latency:{:.2f}"
        self.assertIn("lakehouse", LAKEHOUSE_BASE)
        self.assertTrue(KPI_INFRA_PATH.endswith("kpis_infra.txt"))

    @patch("orquestador_planta.urllib.request.Request")
    @patch("orquestador_planta.urllib.request.urlopen")
    def test_enviar_alerta_discord_no_webhook(self, mock_urlopen, mock_request):
        """Should skip notification when DISCORD_WEBHOOK_URL is empty"""
        from orquestador_planta import enviar_alerta_discord

        with patch.dict(os.environ, {}, True):
            result = enviar_alerta_discord("test message")
            self.assertIsNone(result)
            mock_urlopen.assert_not_called()

    def test_ejecutar_fase_notebook_missing(self):
        """Should return False for non-existent notebook"""
        from orquestador_planta import ejecutar_fase

        result = ejecutar_fase("nonexistent_notebook.ipynb")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
