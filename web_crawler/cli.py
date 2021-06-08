import argparse

from web_crawler.crawler import Crawler


def cli() -> None:
    argument_parser = argparse.ArgumentParser(description="Crawl a website for links.")
    argument_parser.add_argument(
        "url", metavar="url", type=str, help="The URl to begin with"
    )
    arguments = argument_parser.parse_args()
    # remove any trailing slash for consistency:
    crawler = Crawler(start_url=arguments.url.rstrip("/"))

    crawler.validate_start_url()

    print(f"Start URL provided: {crawler.start_url} \n")

    crawler.execute()

    print(
        f"\nFound {len(crawler.parsed_hrefs)} links in {crawler.end_time - crawler.start_time} seconds."
    )


if __name__ == "__main__":
    cli()
