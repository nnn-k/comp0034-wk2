import os

from flask import Flask



def create_app(test_config=None):
    # create the Flask app
    routes = Flask(__name__, instance_relative_config=True)
    # configure the Flask app (see later notes on how to generate your own SECRET_KEY)
    routes.config.from_mapping(
        SECRET_KEY='d',
        # Set the location of the database file called paralympics.sqlite which will be in the app's instance folder
        SQLALCHEMY_DATABASE_URI= "sqlite:///" + os.path.join(routes.instance_path, 'paralympics.sqlite'),  
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        routes.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        routes.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(routes.instance_path)
    except OSError:
        pass


    with routes.app_context():
        # Register the routes with the app in the context
 
        from paralympics import routes

    return routes