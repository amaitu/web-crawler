# web-crawler

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
 - No end-to-end tests
