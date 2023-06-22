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


#@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

#@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))
