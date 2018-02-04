"""
A simple cmd-line utilty to scrape GitHub's search pages.
"""
import sys

from myscrapy.scrapper import GitHubScrapper

if __name__ == '__main__':
    scrapper = GitHubScrapper(sys.argv[1])
    scrapper.scrape()
    scrapper.write_output()
