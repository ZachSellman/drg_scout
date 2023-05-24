"""Simple Flask server that will be expanded later
"""

from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc


app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
db = SQLAlchemy(app)


class Mention(db.Model):
    submission_id = db.Column(db.String(20), primary_key=True)
    post_date = db.Column(db.String(20), nullable=False)
    sub_reddit = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return (
            f"submission_id: {self.submission_id}, "
            "post_date: {self.post_date}, sub_reddit: {self.sub_reddit}"
        )


# Temporary; run this block once then re-comment if db gets deleted.
# with app.app_context():
#     db.create_all()


class GetMentions(Resource):
    def get(self):
        """Get all entries from mentions table

        :return: returns a dict containing all mentions from the db & status
        :rtype: dict, response code
        """
        mentions = Mention.query.all()
        mentions_list = []
        for mention in mentions:
            print(mention)
            mention_data = {
                "submission_id": mention.submission_id,
                "post_date": mention.post_date,
                "sub_reddit": mention.sub_reddit,
            }
            mentions_list.append(mention_data)
        return {"Mentions": mentions_list}, 200


class AddMention(Resource):
    def post(self):
        """Create a new entry to the mentions db table

        :return: returns the added entry and 201, or IntegrityError and 422
        :response object
        """
        if request.is_json:
            mention = Mention(
                submission_id=request.json["submission_id"],
                post_date=request.json["post_date"],
                sub_reddit=request.json["sub_reddit"],
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
                        "sub_reddit": mention.sub_reddit,
                    }
                ),
                201,
            )
        else:
            return {"error": "Request must be JSON"}, 400


api.add_resource(GetMentions, "/")
api.add_resource(AddMention, "/add")


if __name__ == "__main__":
    app.run(debug=True)
