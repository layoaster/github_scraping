"""
Crawler implementations.
"""
import random
import re

import requests


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
        Randomly selects a proxy from the proxy list and builds
        the `proxies` argument of the `Requests` library.

        :return: A random proxy.
        :rtype: dict
        """
        return {'https': 'http://{}'.format(random.choice(self.proxies))}


class GitHubSearchCrawler(BaseCrawler):
    """
    Crawler for GitHub's search page.
    """
    #: Crawler root page target
    ROOT_PAGE = 'https://github.com'
    #: Crawler search page target
    SEARCH_PAGE = 'https://github.com/search'

    def __init__(self, search_keywords, search_type, proxies=None):
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
        scrapped_data = []
        payload = {
            'q': ' '.join(self.search_keywords),
            'type': self.search_type,
            'utf8': '✓'
        }

        response = requests.get(
            self.SEARCH_PAGE,
            params=payload,
            # proxies=self._get_proxy()
        )
        response.encoding = 'utf-8'

        regex_types = {
            'Repositories': (
                r'<ul class=\"repo-list\">(.+?)</ul>',
                r'<h3.+?<a href=\"(.+?)\"'
            ),
            'Issues': (
                r'<div class=\"issue-list\">(.+?)<div class=\"paginate-container\">',
                r'<h3.+?<a href=\"(.+?)\"'
            ),
            'Wikis': (
                r'<div class=\"wiki-list\">(.+?)<div class=\"paginate-container\">',
                r'class=\"h5\".+?<a href=\"(.+?)\"'
            )
        }

        # Capturing block of results
        results_list_re = re.compile(regex_types[self.search_type][0], re.DOTALL)
        results_list = results_list_re.search(response.text).group(1)

        # Capturing each result link
        result_item_re = re.compile(regex_types[self.search_type][1], re.DOTALL)
        result_item_iter = result_item_re.finditer(results_list)
        for match in result_item_iter:
            scrapped_data.append(''.join((self.ROOT_PAGE, match.group(1))))
