from typing import Dict

import pytest

from tests.constants import TEST_DATA_DIR
from web_crawler.crawler import Crawler
from web_crawler.exceptions import InvalidInputException
from web_crawler.link import Link


def test_parse_and_get_links():
    # Arrange
    start_url = "https://sgbarker.com"

    crawler = Crawler(start_url)

    with open(TEST_DATA_DIR.joinpath("index.html")) as file:
        document = file.read()

    # Act
    result = crawler.parse_and_get_links(document, start_url)

    # Assert
    assert len(result) == 3

    assert result == [
        Link(href="https://github.com/amaitu", parent_url=start_url, internal=False),
        Link(
            href="https://unsplash.com/@amaitu", parent_url=start_url, internal=False,
        ),
        Link(
            href="https://sgbarker.com/internal", parent_url=start_url, internal=True,
        ),
    ]


@pytest.mark.parametrize(
    "input",
    [
        {"start_url": "https://example.com"},
        {"start_url": "http://example.com"},
        {"start_url": "https://www.example.com"},
        {"start_url": "http://www.example.com"},
        {"start_url": "https://sub.example.com"},
        {"start_url": "https://visit.london"},
    ],
)
def test_input_validator_returns_true_when_valid(input: Dict[str, str]):
    # Arrange
    crawler = Crawler(**input)
    # Act
    result = crawler.validate_start_url()
    # Assert
    assert result


@pytest.mark.parametrize(
    "input",
    [
        {"start_url": "invalid"},
        {"start_url": " "},
        {"start_url": ""},
        {"start_url": "www.example.com"},
        {"start_url": "example.com"},
        {"start_url": "visit.london"},
    ],
)
def test_input_validator_raises_exception_when_invalid(input: Dict[str, str]):
    # Arrange
    crawler = Crawler(**input)
    # Act
    # Assert
    with pytest.raises(InvalidInputException):
        crawler.validate_start_url()
