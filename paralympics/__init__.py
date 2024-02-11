import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


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


    # Initialise Flask with the SQLAlchemy database extension
    db.init_app(routes)

    # Models are defined in the models module, so you must import them before calling create_all, otherwise SQLAlchemy
    # will not know about them.
    from paralympics.models import User, Region, Event
    # Create the tables in the database
    # create_all does not update tables if they are already in the database.

    # Put the following code inside the create_app function after the code to ensure the instance folder exists
    # This lis likely to be circa line 40.
    with routes.app_context():
        # Register the routes with the app in the context
        db.create_all()
        from paralympics import routes

    return routes