import logging
import time
from typing import Optional
from urllib.parse import urlparse

import requests


def convert_relative_to_absolute_url(base_url, relative_url) -> str:
    base_url_parsed = urlparse(base_url)

    # Relative URLs don't always begin with a '/'.
    if not relative_url.startswith("/"):
        relative_url = "/" + relative_url

    return f"{base_url_parsed.scheme}://{base_url_parsed.netloc}{relative_url}"


def request_document(url: str) -> Optional[str]:
    # in seconds
    time.sleep(0.5)
    print(f"\n fetching url {url}")
    response = requests.get(url, timeout=5)

    if response.status_code not in [200]:
        logging.warning(
            f"Non-200 response, got {str(response.status_code)} from {url}, skipping."
        )
        return None

    if "text/html" not in response.headers["content-type"]:
        logging.warning(
            f"Unsupported content type {response.headers['content-type']} in response from {url}, skipping."
        )
        return None

    return response.text
