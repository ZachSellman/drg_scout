"""Work in progress"""


# from os import getenv
# from dotenv import load_dotenv
# import praw
# import dotenv
# import requests
# from datetime import datetime as dt
# from Drg_class import Drg
# from bot import send

# dotenv.load_dotenv()

# BASE = "http://127.0.0.1:5000/"
# CLIENT_SECRET = getenv("CLIENT_SECRET")
# USERNAME = getenv("NAME")
# PASSWORD = getenv("PASSWORD")
# CLIENT_ID = getenv("CLIENT_ID")
# USER_AGENT = "drg_scout (by u/OmnicBoy)"

# SEARCH_PARAMS = ["drg", "deep rock", "deep rock galactic"]


# def main():
#     REDDIT = praw.Reddit(
#         client_id=CLIENT_ID,
#         client_secret=CLIENT_SECRET,
#         password=PASSWORD,
#         user_agent=USER_AGENT,
#         username=USERNAME,
#     )
#     subreddit = REDDIT.subreddit("all")
#     checked_count = 0
#     for submission in subreddit.stream.submissions():
#         process_submission(submission)
#         checked_count += 1
#         print(checked_count)


# def process_submission(submission):
#     print(f"Submission created at {submission.created_utc}")

#     # for param in SEARCH_PARAMS:
#     # if param in submission.title.lower() or \
#       param in submission.selftext.lower():
#     #     print("Found one!")
#     #     print(
#     #         f"Submission title: {submission.title}, "
# "Submission created at: {submission.created_utc}"
#     #     )


# if __name__ == "__main__":
#     main()
