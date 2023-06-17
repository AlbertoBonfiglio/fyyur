import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
# TODO [X] IMPLEMENT DATABASE URL
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'postgresql://udacity:udacity@localhost:5438/udacity'

# To run migrations:
# flask db init
# flask db migrate -m "<migration description>"
# flask db upgrade
# 
# To revert to previous migration
# flask db downgrade 