"""
Crawler implementations.
"""
import random

GITHUB_TYPES = (
    'Repositories',
    'Wikis',
    'Issues',
)


class BaseCrawler:
    """
    Crawler's base class.
    """
    def __init__(self, proxies):
        """
        Class initialization.

        :param proxies: list of proxies to be used by the crawler.
        :type proxies: list
        """
        self.proxies = proxies

    def _get_proxy(self):
        """
        Randomly selects a proxy from the proxy list.

        :return: A random proxy.
        :rtype: str
        """
        return random.choice(self.proxies)


class GHitHubCrawler(BaseCrawler):
    """
    Crawler for GitHub's search page.
    """
    def __init__(self, search_keywords, search_type, proxies):
        """
        Class initialization.

        :param search_keywords: list of keywords to search for.
        :type search_keywords: list
        :param search_type: Type of search results to retrieve
            (`Repositories`, `Wikis`, `Issues`).
        :type search_type: str
        :param proxies: list of proxies to be used by the crawler.
        :type proxies: list
        """
        super().__init__(proxies)
        self.search_keywords = search_keywords

        if search_type not in GITHUB_TYPES:
            raise ValueError('{} is not a valid type'.format(search_type))
        self.search_type = search_type

    def parse(self):
        """
        Parse search page to gather search results web links.

        :return: results links.
        :rtype: list
        """
        pass
