"""
Set of crawler tests
"""
from unittest.mock import patch

import pytest
from requests.exceptions import ConnectTimeout

from myscrapy.crawler import GitHubSearchCrawler


class TestBaseCrawler:
    """
    Test base
    """
    def test_no_proxy_handling(self, no_proxy_crawler):
        """
        Testing request with no proxies.
        """
        response = no_proxy_crawler.make_request(
            'https://www.google.com',
            payload={'hl': 'en'}
        )
        assert response.status_code == 200
        assert 'Google Search' in response.text

    def test_fail_proxy_handling(self, proxy_crawler):
        """
        Testing request with proxies that fail.
        """
        with pytest.raises(ConnectTimeout):
            proxy_crawler.make_request('https://www.github.com')


class TestGitHubSearchCrawler:
    """
    Set of tests for the GitHub's search page.
    """
    def test_wrong_search_type(self):
        with pytest.raises(ValueError):
            GitHubSearchCrawler(
                GitHubSearchCrawler(
                    ['google', 'cloud'],
                    'invalid-search-type',
                    ['172.0.0.1:8080']
                )
            )

    @pytest.mark.parametrize('load_html', ['search_repo_results.html'], indirect=True)
    def test_repo_results(self, load_html, repo_crawler):
        """
        Testing repository search with results
        """
        with patch('myscrapy.crawler.GitHubSearchCrawler.make_request', return_value=load_html):
            result = repo_crawler.parse()
            assert len(result) == 10
            assert result[0]['url'].startswith('https://github.com/')
            assert ('owner', 'language_stats') == tuple(result[0]['extra'].keys())

    @pytest.mark.parametrize('load_html', ['sample_repo_metadata.html'], indirect=True)
    def test_repo_result_metadata(self, load_html, repo_crawler):
        """
        Testing scraping of a repo metadata
        """
        with patch('myscrapy.crawler.GitHubSearchCrawler.make_request', return_value=load_html):
            lang_stats = repo_crawler._get_repo_metadata('www.test.com')
            assert lang_stats == {'CSS': 1.4, 'HTML': 6.0, 'JavaScript': 90.5, 'Shell': 2.1}

    @pytest.mark.parametrize('load_html', ['search_repo_no_results.html'], indirect=True)
    def test_repo_no_results(self, load_html, repo_crawler):
        """
        Testing repository search with no search results
        """
        with patch('myscrapy.crawler.GitHubSearchCrawler.make_request', return_value=load_html):
            result = repo_crawler.parse()
            assert len(result) == 0

    @pytest.mark.parametrize('load_html', ['search_issue_results.html'], indirect=True)
    def test_issue_results(self, load_html, issue_crawler):
        """
        Testing issue search with results
        """
        with patch('myscrapy.crawler.GitHubSearchCrawler.make_request', return_value=load_html):
            result = issue_crawler.parse()
            assert len(result) == 10
            assert result[0]['url'].startswith('https://github.com/')

    @pytest.mark.parametrize('load_html', ['search_issue_no_results.html'], indirect=True)
    def test_issue_no_results(self, load_html, issue_crawler):
        """
        Testing issue search with no search results
        """
        with patch('myscrapy.crawler.GitHubSearchCrawler.make_request', return_value=load_html):
            result = issue_crawler.parse()
            assert len(result) == 0

    @pytest.mark.parametrize('load_html', ['search_wiki_results.html'], indirect=True)
    def test_wiki_results(self, load_html, wiki_crawler):
        """
        Testing wiki search with results
        """
        with patch('myscrapy.crawler.GitHubSearchCrawler.make_request', return_value=load_html):
            result = wiki_crawler.parse()
            assert len(result) == 10
            assert result[0]['url'].startswith('https://github.com/')
            assert '/wiki/' in result[0]['url']

    @pytest.mark.parametrize('load_html', ['search_wiki_no_results.html'], indirect=True)
    def test_wiki_no_results(self, load_html, wiki_crawler):
        """
        Testing wiki search with no search results
        """
        with patch('myscrapy.crawler.GitHubSearchCrawler.make_request', return_value=load_html):
            result = wiki_crawler.parse()
            assert len(result) == 0
