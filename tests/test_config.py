import unittest

from src import config


class ConfigTests(unittest.TestCase):
    def test_loads_community_pharmacy_keywords_and_title(self):
        self.assertEqual(config.topic_name(), "Community Pharmacy Weekly Letter")
        self.assertEqual(config.report_title(), "Community Pharmacy Weekly Trend Report")
        self.assertIn("GLP-1", config.keywords())
        self.assertIn("NOAC", config.keywords())
        self.assertIn("H. pylori", config.keywords())
        self.assertIn("dentistry", config.keywords())

    def test_journals_include_requested_cardiology_sources(self):
        names = {journal["name"] for journal in config.journals()}
        self.assertIn("JACC (ACC)", names)
        self.assertIn("Circulation (AHA)", names)
        self.assertIn("EHJ (ESC)", names)
        self.assertIn("Europace (EHRA)", names)
