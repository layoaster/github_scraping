"""
Scrapper implementations
"""
import json

from myscrapy.crawler import GitHubSearchCrawler


class GitHubScrapper:
    """
    The Github search page scrapper.
    """
    def __init__(self, settings_file):
        """
        Class initialization.

        :param settings_file: Crawler config file path.
        :type settings_file: str
        """
        with open(settings_file, encoding='utf-8') as json_data:
            self.config = json.load(json_data)

        self.crawler = GitHubSearchCrawler(
            search_keywords=self.config['keywords'],
            search_type=self.config['type'],
            proxies=self.config['proxies']
        )
        self.results = None

    def scrape(self):
        self.results = self.crawler.parse()

    def write_output(self):
        if self.results is not None:
            with open('output.json', 'w', encoding='utf-8') as output_file:
                json.dump(self.results, output_file, indent=3)

