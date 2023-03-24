"""Simple Reddit bot that scans the past 24 hours of data from a subreddit for 
mentions of Deep Rock Galactic.
"""

from os import getenv
from dotenv import load_dotenv
import praw
import dotenv
import requests
from datetime import datetime as dt
from Drg_class import Drg

dotenv.load_dotenv()

BASE = "http://127.0.0.1:5000/"
CLIENT_SECRET = getenv("CLIENT_SECRET")
USERNAME = getenv("NAME")
PASSWORD = getenv("PASSWORD")
CLIENT_ID = getenv("CLIENT_ID")
USER_AGENT = "drg_scout (by u/OmnicBoy)"


def main():

    REDDIT = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        password=PASSWORD,
        user_agent=USER_AGENT,
        username=USERNAME,
    )

    for submission in REDDIT.subreddit("DeepRockGalactic").top(
        time_filter="day", limit=None
    ):
        submission.comments.replace_more(limit=None)
        search_param = "Rock and Stone!"
        if (
            search_param.lower() in submission.title.lower()
            or search_param.lower() in submission.selftext.lower()
        ):
            sub = Drg(
                submission.id, submission.created_utc, submission.subreddit.display_name
            )
            print("Found one in post title/body!")
            send(sub)
            continue

        elif search_param.lower() in [
            comment.body.lower() for comment in submission.comments.list()
        ]:
            sub = Drg(
                submission.id,
                submission.created_utc,
                submission.subreddit.display_name,
            )
            print("Found one in comments!")
            send(sub)

        # for comment in submission.comments.list():
        #     comment_count += 1
        #     if search_param.lower() in comment.body.lower():
        #         sub = Drg(
        #             submission.id,
        #             submission.created_utc,
        #             submission.subreddit.display_name,
        #         )
        #         print("Found one!")
        #         send(sub)
        #         break

    print("All finished!")


def send(obj):
    obj_dict = {
        "submission_id": str(obj.submission_id),
        "post_date": str(obj.time_created),
        "sub_reddit": str(obj.sub_reddit),
    }
    response = requests.post(BASE + "add", json=obj_dict)
    print(f"Added {response.json()}")


if __name__ == "__main__":
    main()
