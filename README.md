# drg_scout

Don't forget to include that people need to initialize their own db file:

with app.app_context():
    db.create_all()
    
This needs to be done after the db.Model has been outlined.
