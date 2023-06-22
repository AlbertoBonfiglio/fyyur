#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from sqlalchemyseeder import ResolvingSeeder
from sqlalchemy.sql import func
from models import db, Venue, Artist, Show

import controllers.venues as vc
import controllers.artist as ac
import controllers.show as sc

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

#----------------------------------------------------------------------------#
# Venue Routes.
#----------------------------------------------------------------------------#
app.add_url_rule('/venues', view_func=vc.venues)
app.add_url_rule('/venues/<int:venue_id>', view_func=vc.show_venue)
app.add_url_rule('/venues/search',view_func=vc.search_venues,  methods=['POST'])
app.add_url_rule('/venues/create', view_func=vc.create_venue_form, methods=['GET'])
app.add_url_rule('/venues/create', view_func=vc.create_venue_submission, methods=['POST'])
app.add_url_rule('/venues/<venue_id>', view_func=vc.delete_venue, methods=['DELETE'])

#----------------------------------------------------------------------------#
# Artist Routes.
#----------------------------------------------------------------------------#
app.add_url_rule('/artists', view_func=ac.artists)
app.add_url_rule('/artists/<int:artist_id>', view_func=ac.show_artist)
app.add_url_rule('/artists/<int:artist_id>/edit', view_func=ac.show_artist, methods=['GET'])
app.add_url_rule('/artists/<int:artist_id>/edit', view_func=ac.show_artist, methods=['POST'])
app.add_url_rule('/artists/search',view_func=ac.search_artists,  methods=['POST'])
app.add_url_rule('/artists/create', view_func=ac.create_artist_form, methods=['GET'])
app.add_url_rule('/artists/create', view_func=ac.create_artist_submission, methods=['POST'])
app.add_url_rule('/artists/<artist_id>', view_func=ac.delete_artist, methods=['DELETE'])


#----------------------------------------------------------------------------#
# Show Routes
#----------------------------------------------------------------------------#
app.add_url_rule('/shows', view_func=sc.shows)
#app.add_url_rule('/shows/<int:show_id>', view_func=sc.show_show)
#app.add_url_rule('/shows/<int:show_id>/edit', view_func=sc.show_show, methods=['GET'])
#app.add_url_rule('/shows/<int:show_id>/edit', view_func=sc.show_show, methods=['POST'])
#app.add_url_rule('/shows/search',view_func=sc.search_shows,  methods=['POST'])
#app.add_url_rule('/shows/create', view_func=sc.create_show_form, methods=['GET'])
app.add_url_rule('/shows/create', view_func=sc.create_show_submission, methods=['POST'])
app.add_url_rule('/shows/<show_id>', view_func=sc.delete_show, methods=['DELETE'])



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
def seed(): 
  _count=0
  try:
    db.session.expire_all()
    venues = db.session.query(func.count(Venue.id)).scalar()
    if venues < 1 :
      print(f'Found no venues. Seeding....')
      seeder = ResolvingSeeder(db.session)
      seeder.register_class(Venue)
      seeder.register_class(Artist)
      seeder.register_class(Show)
      print(f'Loading data..')
      # See API reference for more options
      new_entities = seeder.load_entities_from_json_file('./seed.json', separate_by_class=True, flush_on_create=True, commit=False)
      _count = len(new_entities)
      print(f'Seeding {_count} entities...')
      # _count = new_entities.
      db.session.commit()
    else:  
      print(f'Found {venues} venues.')
  except Exception as ex:
    print(ex)
    db.session.rollback  
  finally:
    print(f'Seeding complete. {_count} Entities inserted.')
    
seed()

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


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

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
