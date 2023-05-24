from datetime import datetime as dt


class Drg:
    def __init__(self, submission_id, time_created, subreddit):
        self.submission_id = submission_id
        self.time_created = dt.fromtimestamp(time_created)
        self.subreddit = subreddit

    def __repr__(self):
        return (
            f"submission_id = {self.submission_id}, "
            "time_created = {self.time_created}, subreddit = {self.sub_reddit}"
        )
