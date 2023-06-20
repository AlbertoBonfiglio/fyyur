
#from app import app
from models import db, Venue, Show
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_wtf import Form
from forms import VenueForm

def venues():
  # TODO: replace with real venues data.
  # Aggregate by state and city
  # num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  _data = []  
  qryStr = '''select v.city as city, v.state as state, v.id as venue_id, v.name, count(s.upcoming) as upcoming
              from ( 
                select ss.venue_id, (ss.start_time > now()) as upcoming
                from public."Show" ss 
                group by ss.venue_id, ss.start_time
                having ss.start_time > now()
              ) as s
              right join public."Venue" v 
              on v.id = s.venue_id
              group by v.city, v.state, v.name, v.id, s.upcoming
              order by v.state, v.city, v.name, v.id, s.upcoming'''
  
  rows = db.session.execute(qryStr).all()
  # find if state and city already there
  # if not adds an entry and inserts the first venue
  # if yes adds the venue
  for row in rows:
    item = [item for item in _data if (item.get('city') == row.city and item.get('state') == row.state)]
    if (len(item) == 0):
      _data.append({
        "city": row.city,
        "state": row.state,
        "venues": [{
          "id": row.venue_id,
          "name": row.name,
          "num_upcoming_shows": row.upcoming,
        }]
      })
    else :
      item[0].get('venues').append({
          "id": row.venue_id,
          "name": row.name,
          "num_upcoming_shows": row.upcoming,
      })
  
  return render_template('pages/venues.html', areas=_data);



def search_venues():
  # TODO [ ]: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO[X] : replace with real venue data from the venues table, using venue_id #
  data = Venue.query.get(venue_id);
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)


def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None
