# drg_scout

This particular bot utilizes PRAW and Flask/SQLite to parse incoming posts/comments to the website Reddit. The bots parse for a specific string, and send POST requests to the Flask RESTful api, which passes the information to the db for storage, and returns a status.
