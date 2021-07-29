# web-crawler
Takes an input URL and crawls it, outputting all the links found on that page. Will then crawl other urls found on that page, provided they are on the same domain. Subdomains are treated as different domains. 

## To install
1. Install [Poetry](https://python-poetry.org/docs/) and [Python >= 3.7](https://www.python.org/downloads/) on your system.
2. Run `poetry install`

## To run the crawler
`poetry run python web_crawler/cli.py https://sgbarker.com`

## To run the tests
`poetry run pytest --cov=web_crawler tests/`

## Known limitations / gotchas
 - The crawler will treat mixed content links as external, i.e. `http` links on a `https` page.
 - No backoff / handling of 429s or other non-200 responses.
 - Unit test coverage on crawler could be improved.
 - No end-to-end tests.
