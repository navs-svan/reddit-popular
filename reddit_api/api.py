from dotenv import load_dotenv
from pathlib import Path
import os
import requests
import sys
import json


class RedditScraper:
    def __init__(self, **credentials):
        self.credentials = credentials
        self.headers = self.get_authentication()
        print(self.headers)

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
        r = requests.get(endpoint, headers=self.headers)

        return r.json()


if __name__ == "__main__":

    env_path = Path().resolve().parent / ".env"
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
