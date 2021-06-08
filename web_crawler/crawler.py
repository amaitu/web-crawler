import logging
import re
import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue, Empty
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from web_crawler.exceptions import InvalidInputException
from web_crawler.helpers import convert_relative_to_absolute_url, request_document
from web_crawler.link import Link


class Crawler:
    def __init__(self, start_url: str):
        self.start_url = start_url
        self.start_time = None
        self.end_time = None
        self.pool = ThreadPoolExecutor(max_workers=10)
        self.processed_links = set()
        self.parsed_hrefs = []
        self.unprocessed_links = Queue()
        # Start the queue with the initial URl
        self.unprocessed_links.put(
            Link(href=start_url, parent_url=start_url, internal=True,)
        )

    def parse_and_get_links(self, html_content: str, parent_url: str) -> List[Link]:
        soup = BeautifulSoup(html_content, "html.parser")
        results = []
        for link in soup.find_all("a", href=True):
            href = link.get("href")

            if href.startswith("#"):
                continue

            # if it's a relative url, concatenate the relative url to the start_url to make it absolute:
            if not href.startswith("http"):
                href = convert_relative_to_absolute_url(self.start_url, href)

            results.append(
                Link(
                    href=href.rstrip("/"),
                    internal=True if self.start_url in href else False,
                    parent_url=parent_url,
                )
            )
        return results

    def execute(self) -> None:
        self.start_time = time.time()

        while True:
            try:
                link = self.unprocessed_links.get(timeout=1)
                if link.href not in self.processed_links:
                    self.processed_links.add(link.href)
                    self.pool.submit(self.crawl, link.href)

            except Empty:
                self.end_time = time.time()
                return

    def crawl(self, url: str) -> None:
        html_content = request_document(url)

        if not html_content:
            return

        for link in self.parse_and_get_links(html_content=html_content, parent_url=url):
            link.display()
            self.parsed_hrefs.append(link.href)

            if link.internal and link.href not in self.processed_links:
                self.unprocessed_links.put(link)

    def validate_start_url(self) -> bool:
        if not self.start_url:
            raise InvalidInputException("No URL provided.")

        if not re.match(
            # adapted from https://stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url :
            r"https?://(www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,10}\b([-a-zA-Z0-9()@:%_+.~#?&//=]*)",
            self.start_url,
        ):
            raise InvalidInputException(
                f"Start URL provided ({self.start_url}) appears to be invalid. Did you include the http(s):// at the start?"
            )

        return True
