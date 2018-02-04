# GitHub's search page Crawler
A handmade Github's search page scrapper. The scrapper returns a list of
URL's for each result listed on the first page. **Only** repositories,
issues, or wikis are supported.

## Requirements:

1. Python 3.6.x

## Installation & usage

1. Install package requirements.

```bash
pip install -r requirements.txt
```

2. Run the scrapper providing a JSON config file.

```bash
python github_scraping.py input.json
```

The JSON config file needs to provide the following paramaters:

* `keywords`: The search keywords.
* `type`: The kind of search to perform. It can be one of theses:
`Repositories`,`Wikis` or `Issues`
* `proxies`: A list of proxies to be used randomly by the crawler.

A sample config file:

```json
{
  "keywords": [
    "google",
    "cloud"
  ],
  "proxies": [
    "89.236.17.108:3128",
    "51.15.205.156:3128",
    "163.172.27.213:3128",
    "185.82.212.95:8080",
    "45.77.122.154:80",
    "147.135.210.114:54566",
    "185.93.3.123:8080"
  ],
  "type": "Issues"
}
```

The scrapper writes results to a file named `output.json`. It should
look like this:

```json
[
   {
      "url": "https://github.com/CC-Exercises/exercise-11-task-03-cc-exercise11-task3-jg/pull/1"
   },
   {
      "url": "https://github.com/ryankikta/Printaura/issues/13"
   },
   {
      "url": "https://github.com/ryankikta/Printaura/issues/2"
   },
   {
      "url": "https://github.com/h4cc/awesome-elixir/issues/4399"
   },
   {
      "url": "https://github.com/ggchan0/CPE_350/issues/25"
   },
   {
      "url": "https://github.com/graphcool/prisma/issues/1708"
   },
   {
      ...
   }
]
```

For repository searches the output should look like:

```json
[
   {
      "url": "https://github.com/liberodark/ODrive",
      "extra": {
         "owner": "liberodark",
         "language_stats": {
            "JavaScript": 90.5,
            "HTML": 6.0,
            "Shell": 2.1,
            "CSS": 1.4
         }
      }
   },
   {
      "url": "https://github.com/ilyas-it83/CloudComparer",
      "extra": {
         "owner": "ilyas-it83",
         "language_stats": {
            "CSS": 65.7,
            "HTML": 34.0,
            "JavaScript": 0.3
         }
      }
   },
   {
      "url": "https://github.com/bazelbuild/rules_docker",
      "extra": {
         "owner": "bazelbuild",
         "language_stats": {
            "Python": 88.8,
            "Shell": 7.2,
            "Java": 1.1,
            "C++": 0.8,
            "Scala": 0.6,
            "Groovy": 0.6,
            "Other": 0.9
         }
      }
   },
   {
      "url": "https://github.com/GoogleCloudPlatform/cloud-trace-java",
      "extra": {
         "owner": "GoogleCloudPlatform",
         "language_stats": {
            "Java": 100.0
         }
      }
   },
   {
      "url": "https://github.com/geeknam/python-gcm",
      "extra": {
         "owner": "geeknam",
         "language_stats": {
            "Python": 100.0
         }
      }
   },
   {
      ...
   }
]
```

## ToDo's

* Unittesting.
* Better handling of network-related errors.
* Scrapper a given number of search results pages.
