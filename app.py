"""Flask server which provides RESTful API for interaction between\
reddit trawlers and database to store collected data
"""

from flask import Flask, request, jsonify, make_response, abort
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc


app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
db = SQLAlchemy(app)


class Mention_Model(db.Model):
    submission_id = db.Column(db.String(20), primary_key=True)
    post_date = db.Column(db.String(20), nullable=False)
    subreddit = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return (
            f"submission_id: {self.submission_id}, "
            "post_date: {self.post_date}, subreddit: {self.subreddit}"
        )


# Temporary; run this block once then re-comment if db gets deleted.
# with app.app_context():
#     db.create_all()
def abort_if_no_submission_id(submission_id):
    """Checks if the submission_id exists in the DB

    :param submission_id: submission_id of specific mention
    :type submission_id: string
    """
    if not db.session.execute(
        db.select(Mention_Model).filter_by(submission_id=submission_id)
    ):
        abort(404, message=f"submission_id {submission_id} doesn't exist")


class Mentions(Resource):
    def get(self, submission_id):
        """Returns mention based on submission_id.

        :param submission_id: submission_id of specific mention
        :type submission_id: string
        :return: json formatted mention result
        :rtype: json
        """
        abort_if_no_submission_id(submission_id)
        mention = db.get_or_404(Mention_Model, submission_id)
        mention_dict = {
            "submission_id": mention.submission_id,
            "post_date": mention.post_date,
            "subreddit": mention.subreddit,
        }

        return {"mention": mention_dict}, 200


class Mentions_List(Resource):
    def get(self):
        """Get all entries from mentions table

        :return: returns a dict containing all mentions from the db & status
        :rtype: json response, response code
        """
        mentions = Mention_Model.query.all()
        mentions_list = []
        for mention in mentions:
            print(mention)
            mention_data = {
                "submission_id": mention.submission_id,
                "post_date": mention.post_date,
                "subreddit": mention.subreddit,
            }
            mentions_list.append(mention_data)
        return {"Mentions_List": mentions_list}, 200

    def post(self):
        """Create a new entry to the mentions db table

        :return: returns the added entry and 201, or IntegrityError and 422
        :response object
        """
        if request.is_json:
            mention = Mention_Model(
                submission_id=request.json["submission_id"],
                post_date=request.json["post_date"],
                subreddit=request.json["subreddit"],
            )
            try:
                db.session.add(mention)
                db.session.commit()

            except exc.IntegrityError:
                return (
                    {
                        "error": (
                            "IntegrityError: unique constraint failed; "
                            "mention already exists in database."
                        )
                    },
                    422,
                )

            return make_response(
                jsonify(
                    {
                        "submission_id": mention.submission_id,
                        "post_date": mention.post_date,
                        "subreddit": mention.subreddit,
                    }
                ),
                201,
            )
        else:
            return {"error": "Request must be JSON"}, 400


api.add_resource(Mentions, "/mentions/<string:submission_id>")
api.add_resource(Mentions_List, "/mentions/all")


if __name__ == "__main__":
    app.run(debug=True)
