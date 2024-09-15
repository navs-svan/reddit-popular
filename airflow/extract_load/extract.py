import csv
import json
import os
import pandas as pd
from datetime import datetime
from multiprocessing import Process

from pathlib import Path
from dotenv import load_dotenv
from reddit_api.api import RedditScraper

from reddit_scraper.spiders.redspider import RedspiderSpider
from scrapy.crawler import CrawlerProcess


def transform_data(json_data: json, cur_date: str):
    details_dict = {
        "title": json_data[0]["data"]["children"][0]["data"]["title"],
        "subreddit": json_data[0]["data"]["children"][0]["data"][
            "subreddit_name_prefixed"
        ],
        "author": json_data[0]["data"]["children"][0]["data"]["author"],
        "url": json_data[0]["data"]["children"][0]["data"]["permalink"],
        "nsfw": json_data[0]["data"]["children"][0]["data"]["over_18"],
        "score": json_data[0]["data"]["children"][0]["data"]["score"],
        "self_text": json_data[0]["data"]["children"][0]["data"]["selftext"],
        "upvote_ratio": json_data[0]["data"]["children"][0]["data"]["upvote_ratio"],
        "awards": json_data[0]["data"]["children"][0]["data"]["total_awards_received"],
        "time": json_data[0]["data"]["children"][0]["data"]["created"],
        "date_popular": cur_date,
    }

    return details_dict


def save_data(transformed_data: list, filename: Path):
    df = pd.DataFrame(transformed_data)
    df.to_parquet(filename)


def execute_crawling(country: str, cur_date: str, filepath: Path, app: RedditScraper):
    settings = {
        "FEEDS": {
            f"{filepath.parent}/{country}.csv": {"format": "csv", "overwrite": True},
        },
        "CLOSESPIDER_PAGECOUNT": 4,
        "DOWNLOAD_DELAY": 5,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 16,
    }
    process = CrawlerProcess(settings)
    process.crawl(RedspiderSpider, country=country)
    process.start()

    if not os.path.exists("local_data"):
        os.makedirs("local_data")

    with open(filepath.parent / f"{country}.csv", "r", encoding="utf8") as f:
        links = csv.reader(f)
        next(links, None)

        dict_list = [
            transform_data(app.get_post_details(link[0]), cur_date) for link in links
        ]

        filename = filepath.parent / "local_data" / f"{country}_{cur_date}.parquet"
        save_data(dict_list, filename)

    os.remove(filepath.parent / f"{country}.csv")


if __name__ == "__main__":
    filepath = Path(__file__).resolve()
    env_path = filepath.parent.parent / ".env"
    env_file = load_dotenv(env_path)

    credential = {
        "CLIENT_ID": os.environ.get("CLIENT_ID"),
        "SECRET_TOKEN": os.environ.get("SECRET_TOKEN"),
        "REDDIT_USER": os.environ.get("REDDIT_USER"),
        "REDDIT_PASS": os.environ.get("REDDIT_PASS"),
    }

    app = RedditScraper(**credential)

    # scrape links from r/popular using scraper

    countries = ("PH", "global", "MY", "SG", "TH")
    cur_date = datetime.today().strftime("%Y-%m-%d")

    for country in countries:
        p = Process(target=execute_crawling, args=(country, cur_date, filepath, app))
        p.start()
        p.join()
