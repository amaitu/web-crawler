from unittest.mock import patch

import pytest

from web_crawler.helpers import convert_relative_to_absolute_url, request_document


@patch('web_crawler.helpers.requests.get')
def test_request_document_ok(mock_get):
    # Arrange:
    url = "https://example.com"
    html = "<!doctype html><html></html>"

    mock_get.return_value.ok = True
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = html
    mock_get.return_value.headers = {"content-type": "text/html"}

    # Act:
    result = request_document(url)

    # Assert:
    assert result == html


@patch('web_crawler.helpers.requests.get')
def test_request_document_ok_invalid_content_type(mock_get):
    # Arrange:
    url = "https://example.com"
    json = "{}"

    mock_get.return_value.ok = True
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = json
    mock_get.return_value.headers = {"content-type": "application/sjon"}

    # Act:
    result = request_document(url)

    # Assert:
    assert not result


@patch('web_crawler.helpers.requests.get')
def test_request_document_not_ok(mock_get):
    # Arrange:
    url = "https://example.com"
    html = "<!doctype html><html></html>"

    mock_get.return_value.ok = True
    mock_get.return_value.status_code = 429
    mock_get.return_value.text = html
    mock_get.return_value.headers = {"content-type": "text/html"}

    # Act:
    result = request_document(url)

    # Assert:
    assert not result


@pytest.mark.parametrize(
    "base_url,comparison_url,expected",
    [
        ("https://sgbarker.com", "/about/", "https://sgbarker.com/about/"),
        ("https://sgbarker.com", "about/", "https://sgbarker.com/about/"),
        (
                "https://en.wikipedia.org",
                "/wiki/Ludovic_Laborderie",
                "https://en.wikipedia.org/wiki/Ludovic_Laborderie",
        ),
        (
                "https://www.sgbarker.com",
                "about/contact/something",
                "https://www.sgbarker.com/about/contact/something",
        ),
    ],
)
def test_convert_relative_to_absolute_url(base_url, comparison_url, expected):
    assert convert_relative_to_absolute_url(base_url, comparison_url) == expected
