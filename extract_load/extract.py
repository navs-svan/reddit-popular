import csv
import json
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from reddit_api.api import RedditScraper

from reddit_scraper.spiders.redspider import RedspiderSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


if __name__ == "__main__":
    filepath = Path(__file__).resolve()
    env_path = filepath.parent.parent / ".env"
    env_file = load_dotenv(env_path)
    cur_date = datetime.today().strftime("%Y-%m-%d")

    credential = {
        "CLIENT_ID": os.environ.get("CLIENT_ID"),
        "SECRET_TOKEN": os.environ.get("SECRET_TOKEN"),
        "REDDIT_USER": os.environ.get("REDDIT_USER"),
        "REDDIT_PASS": os.environ.get("REDDIT_PASS"),
    }

    app = RedditScraper(**credential)

    # scrape links from r/popular using scraper

    country="PH"

    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(RedspiderSpider, country=country)
    process.start()

    if not os.path.exists("local_data"):
        os.makedirs("local_data")

    with open(filepath / "data.csv", "r", encoding="utf8") as f:
        links = csv.reader(f)
        next(links, None)

        for link in links:
            details = app.get_post_details(link[0])
            filename = filepath / "local_data" / f"{link[0].replace('/', '_')}{cur_date}.json"
            with open(filename, "w") as f:
                json.dump(details, f, indent=4)
