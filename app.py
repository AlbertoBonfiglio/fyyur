#----------------------------------------------------------------------------# 
# REMOVE ME
# source /home/darthbert/workspaces/udacity/fyyur/.venv/bin/activate
#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import dateutil.parser
import babel
from flask import Flask
from flask_moment import Moment
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from forms import *
from models import db
import seed as seeder
import routes as router

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
# TODO [X] : connect to a local postgresql database
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.app = app
db.init_app(app)
migrate = Migrate(app, db)
router.config_routes(app)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#
def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value) if isinstance(value, str) else value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en') # type: ignore

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Seed DB if necessary
#----------------------------------------------------------------------------#
seeder.seed()

#----------------------------------------------------------------------------#
# Configure debug
#----------------------------------------------------------------------------#
if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# TODO [ ]  Implement artist availability. An artist can list available times that they can be booked. Restrict venues from being able to create shows with artists during a show time that is outside of their availability.
# TODO [ ]  Implement Search Artists by City and State, and Search Venues by City and State. Searching by "San Francisco, CA" should return all artists or venues in San Francisco, CA.


# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
