import asyncio
import unittest
from urllib.parse import quote_plus

from src import webscraper


class _FakeResponse:
    status_code = 200
    text = "<rss><channel></channel></rss>"


class _FakeClient:
    def __init__(self):
        self.urls = []

    async def get(self, url, timeout=20):
        self.urls.append(url)
        return _FakeResponse()


class WebscraperTests(unittest.TestCase):
    def test_parse_rss_items_filters_with_topic_keywords(self):
        xml = """
        <rss><channel>
          <item>
            <title>Semaglutide update for community pharmacy diabetes care</title>
            <link>https://example.com/a</link>
            <description>GLP-1 counselling and adherence tips</description>
          </item>
          <item>
            <title>Quarterly real estate market report</title>
            <link>https://example.com/b</link>
            <description>Unrelated content</description>
          </item>
        </channel></rss>
        """

        articles = webscraper._parse_rss_items(xml, "Test", topic_filter=True)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].source, "Test")
        self.assertIn("semaglutide", [tag.lower() for tag in articles[0].tags])

    def test_google_news_uses_source_query(self):
        src = {
            "name": "Medscape Cardiology",
            "domain": "medscape.com",
            "query": "NOAC OR statin OR heart failure",
            "max_items": 5,
        }
        client = _FakeClient()

        asyncio.run(webscraper._fetch_google_news(client, src))

        expected_q = quote_plus("site:medscape.com NOAC OR statin OR heart failure")
        self.assertTrue(client.urls)
        self.assertIn(f"q={expected_q}", client.urls[0])

    def test_markdown_output_no_longer_mentions_breast_cancer(self):
        results = {
            "FDA Drug Safety": [
                webscraper.Article(
                    title="FDA warns about interaction between two common medicines",
                    url="https://example.com",
                    source="FDA Drug Safety",
                    published="2026-04-25",
                    tags=["drug interaction"],
                )
            ]
        }

        markdown = webscraper.format_articles_md(results)

        self.assertIn("### FDA Drug Safety（1 篇相關文章）", markdown)
        self.assertNotIn("乳癌", markdown)
