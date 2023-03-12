"""Simple Reddit bot that scans the past 24 hours of data from a subreddit for 
mentions of Deep Rock Galactic.
"""

from os import getenv
from dotenv import load_dotenv
import praw
import dotenv

dotenv.load_dotenv()

CLIENT_SECRET = getenv("CLIENT_SECRET")
USERNAME = getenv("NAME")
PASSWORD = getenv("PASSWORD")
CLIENT_ID = getenv("CLIENT_ID")
USER_AGENT = "drg_scout (by u/OmnicBoy)"

REDDIT = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    password=PASSWORD,
    user_agent=USER_AGENT,
    username=USERNAME,
)


class Drg:
    def __init__(self, sub_id, time_created):
        self.sub_id = sub_id
        self.time_created = time_created

    def __str__(self):
        return f"Butts"


def main():
    sub_count = 0
    comment_count = 0
    for submission in REDDIT.subreddit("Pokemon").top(time_filter="day", limit=None):
        sub_count += 1
        submission.comments.replace_more(limit=None)
        search_pram = "Pikachu"
        if (
            search_pram.lower() in submission.title.lower()
            or search_pram.lower() in submission.selftext.lower()
        ):
            sub = Drg(submission.id, submission.created_utc)
            print("Found one!")
            send(sub)
            break

        for comment in submission.comments.list():
            comment_count += 1
            if search_pram.lower() in comment.body.lower():
                sub = Drg(submission.id, submission.created_utc)
                print("Found one!")
                send(sub)
                break

    print(f"All finished! \n comment count = {comment_count}, sub_count = {sub_count}")


def send(obj):
    """Temporary function, will eventually send a POST request to app.py's server

    :param obj: object instatiated during main()'s searching
    :type obj: instance object
    """
    print(f"Here is the output!: {obj}")


if __name__ == "__main__":
    main()
