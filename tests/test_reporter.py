import unittest
from unittest import mock

from src import reporter


class ReporterTests(unittest.TestCase):
    def test_empty_report_uses_community_pharmacy_title(self):
        with mock.patch("src.reporter.db.get_tweets_since", return_value=[]), mock.patch(
            "src.reporter.db.get_accounts", return_value=[]
        ):
            report = reporter.build_report(days=7)

        self.assertTrue(report.startswith("# Community Pharmacy Weekly Trend Report"))
        self.assertNotIn("Breast Cancer", report)
