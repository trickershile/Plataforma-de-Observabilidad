import os
import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "notebooks"))


class TestDashboard(unittest.TestCase):
    """Unit tests for app_dashboard.py configuration"""

    def test_rutas_configurables(self):
        """Verify LAKEHOUSE_PATH env var overrides default path"""
        test_path = "/custom/lakehouse"
        with patch.dict(os.environ, {"LAKEHOUSE_PATH": test_path}, clear=False):
            import importlib
            import app_dashboard as ad
            importlib.reload(ad)
            self.assertIn(test_path, ad.RUTA_GOLD)
            self.assertIn(test_path, ad.KPI_INFRA_PATH)

    def test_alert_log_path_env_var(self):
        """Verify LOG_FILE_PATH env var is used when set"""
        test_log = "/app/alertas.log"
        with patch.dict(os.environ, {"LOG_FILE_PATH": test_log}, clear=False):
            import importlib
            import app_dashboard as ad
            importlib.reload(ad)
            self.assertEqual(ad.ALERT_LOG_PATH, test_log)

    def test_rutas_default_auto_detect(self):
        """Verify default paths auto-detect based on script location"""
        saved_lakehouse = os.environ.pop("LAKEHOUSE_PATH", None)
        saved_log = os.environ.pop("LOG_FILE_PATH", None)
        try:
            import importlib
            import app_dashboard as ad
            importlib.reload(ad)
            self.assertTrue(os.path.isabs(ad.RUTA_BASE))
            self.assertIn("lakehouse", ad.RUTA_BASE)
            self.assertIn("alertas.log", ad.ALERT_LOG_PATH)
        finally:
            if saved_lakehouse is not None:
                os.environ["LAKEHOUSE_PATH"] = saved_lakehouse
            if saved_log is not None:
                os.environ["LOG_FILE_PATH"] = saved_log

    def test_f1_score_calculation(self):
        """Verify F1 score computation with known values"""
        from sklearn.metrics import f1_score

        y_true = [0, 0, 1, 0, 1, 0, 0]
        y_pred = [0, 0, 1, 0, 0, 0, 0]
        score = f1_score(y_true, y_pred)
        self.assertAlmostEqual(score, 0.6667, places=3)


if __name__ == "__main__":
    unittest.main()
