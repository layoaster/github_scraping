"""
Crawler implementations.
"""
import random
import re

import requests
from requests.exceptions import ProxyError


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

    def _make_request(self, url, payload=None):
        """
        Make the HTTP GET request handling proxy errors.

        :param url: URL to make the HTTP GET request.
        :type url: str
        :param payload: Parameter to pass to the GET request.
        :type payload: dict
        :return the Response object.
        :rtype: :class:`requests.Response`
        """
        response = None
        while 1:
            try:
                response = requests.get(
                    url,
                    params=payload,
                    proxies=self._get_proxy()
                )
            except ProxyError:
                print("Proxy error, attempting again ...")
            else:
                break

        response.encoding = 'utf-8'

        return response

    def _get_repo_metadata(self, url):
        """
        Parses a repository page to get the languages stats.

        :param url: Repository's URL
        :return: Repository's stats.
        :rtype: dict
        """
        response = self._make_request(url)

        # Capturing block of language stats
        languages_re = re.compile(r'<span class=\"lang\">(.+?)<.+?percent">(.+?)%', re.DOTALL)
        languages_iter = languages_re.finditer(response.text)

        lang_stats = {}
        for match in languages_iter:
            lang_stats[match.group(1)] = float(match.group(2))

        return lang_stats

    def parse(self):
        """
        Parse search page to gather search results web links.

        :return: results links.
        :rtype: list
        """
        payload = {
            'q': ' '.join(self.search_keywords),
            'type': self.search_type,
            'utf8': '✓'
        }
        response = self._make_request(self.SEARCH_PAGE, payload=payload)

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
        try:
            results_list = results_list_re.search(response.text).group(1)
        except AttributeError:
            return []

        # Capturing each result link
        result_item_re = re.compile(regex_types[self.search_type][1], re.DOTALL)
        result_item_iter = result_item_re.finditer(results_list)

        scrapped_data = []
        for match in result_item_iter:
            result_metadata = {
                'url': ''.join((self.ROOT_PAGE, match.group(1)))
            }
            # Retrieving repo stats
            if self.search_type == 'Repositories':
                extras = {
                    'owner': result_metadata['url'].split('/')[3],
                    'language_stats': self._get_repo_metadata(result_metadata['url'])
                }
                result_metadata['extra'] = extras

            scrapped_data.append(result_metadata)

        return scrapped_data
