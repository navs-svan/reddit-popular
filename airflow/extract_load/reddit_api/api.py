from dotenv import load_dotenv
from pathlib import Path
import os
import requests
import sys
import json
import time


class RedditScraper:
    def __init__(self, **credentials):
        self.credentials = credentials
        self.headers = self.get_authentication()

    def get_authentication(self):
        """get temporary reddit api OAuth"""
        # taken from https://www.youtube.com/watch?v=FdjVoOf9HN4

        auth = requests.auth.HTTPBasicAuth(
            self.credentials["CLIENT_ID"], self.credentials["SECRET_TOKEN"]
        )
        data = {
            "grant_type": "password",
            "username": self.credentials["REDDIT_USER"],
            "password": self.credentials["REDDIT_PASS"],
        }
        headers = {"User-Agent": "My-API/0.0.1"}

        try:
            res = requests.post(
                "https://www.reddit.com/api/v1/access_token",
                auth=auth,
                data=data,
                headers=headers,
            )
        except:
            print("ERROR IN ACCESSING TOKEN")
            sys.exit()

        token = res.json()["access_token"]
        headers = {**headers, **{"Authorization": f"bearer {token}"}}

        return headers

    def get_post_details(self, link):
        """gets post details and saves it to the database"""

        endpoint = "https://oauth.reddit.com" + link
        r = self.reddit_request(endpoint)

        return r.json()

    def reddit_request(self, link):
        for _ in range(3):
            try:
                r = requests.get(link, headers=self.headers, timeout=30)
            except requests.exceptions.Timeout as err:
                time.sleep(5)
            except requests.exceptions.RequestException as err:
                print(err)
                sys.exit()
            else:
                return r


if __name__ == "__main__":

    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    env_file = load_dotenv(env_path)

    credential = {
        "CLIENT_ID": os.environ.get("CLIENT_ID"),
        "SECRET_TOKEN": os.environ.get("SECRET_TOKEN"),
        "REDDIT_USER": os.environ.get("REDDIT_USER"),
        "REDDIT_PASS": os.environ.get("REDDIT_PASS"),
    }

    app = RedditScraper(**credential)
    link = "/r/ChikaPH/comments/1fa7jf0/elaiza_and_karl_yulo/"

    details = app.get_post_details(link)
    with open("data.json", "w") as f:
        json.dump(details, f, indent=4)
