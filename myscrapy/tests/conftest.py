"""
Fixtures
"""
import pytest
from unittest.mock import Mock

from myscrapy.crawler import BaseCrawler, GitHubSearchCrawler


@pytest.fixture(scope="function")
def load_html(request):
    """
    Creates a fake `Response` object from a HTML file loaded as a fixture.

    :param request: Filename of the HTML page to be loaded.
    :type request: str
    :return: The `Response` object from a fixture.
    :rtype: :class:`requests.Response`
    """
    import os
    from requests import Response

    # Loading HTML fixture
    base_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(base_dir, 'html', request.param)
    file_content = open(file_path, 'r', encoding='utf-8').read()

    # Loading fixture content into the Response object
    response = Mock(spec=Response)
    response.status_code = 200
    response.encoding = 'utf-8'
    response.text = file_content

    return response


@pytest.fixture(scope="module")
def repo_crawler():
    return GitHubSearchCrawler(
        ['google', 'cloud'],
        'Repositories',
        None
    )


@pytest.fixture(scope="module")
def issue_crawler():
    return GitHubSearchCrawler(
        ['google', 'cloud'],
        'Issues',
        None
    )


@pytest.fixture(scope="module")
def wiki_crawler():
    return GitHubSearchCrawler(
        ['google', 'cloud'],
        'Wikis',
        None
    )


@pytest.fixture(scope="module")
def no_proxy_crawler():
    return BaseCrawler(None)


@pytest.fixture(scope="module")
def proxy_crawler():
    return BaseCrawler(['135.162.160.108:8080'])

