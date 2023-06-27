from models import db, Venue, Show
from flask import render_template, request,jsonify, make_response, flash, redirect, url_for, abort
from forms import VenueForm
from sqlalchemy import delete
import sys

def venues():
  # TODO [X]: replace with real venues data.
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
  # TODO [X]: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  qry = request.form.get('search_term', '')
  data = Venue.query.filter(Venue.name.ilike(f'%{qry}%')).all()
  response={
    "count": len(data),
    "data": data
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO [X] : replace with real venue data from the venues table, using venue_id #
  data: Venue = Venue.query.get(venue_id);
  return render_template('pages/show_venue.html', venue=data)


def delete_venue(venue_id):
  # TODO [X]: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  db.session.begin()
  response = make_response(
    jsonify({"redirect": url_for('index') }),
    200
  )
  try:
    m2m = delete(Show).where(Show.venue_id == venue_id)
    qry = delete(Venue).where(Venue.id == venue_id)
    db.session.execute(m2m)
    db.session.execute(qry)
    db.session.commit()
    
    flash(f'Venue {venue_id} deleted.')    
  except Exception as err:
    flash(f'An error occurred. Venue {venue_id} could not be deleted.')
    response = make_response(
      jsonify({"err": getattr(err, 'message', repr(err)) }),
      500
    )
    db.session.rollback()
  finally:
    db.session.close()
  response.headers["Content-Type"] = "application/json"  
  return response


#  Create Venue
#  ----------------------------------------------------------------
def create_venue_form():
  form: VenueForm = VenueForm()
  return render_template('forms/new_venue.html', form=form)


def create_venue_submission():
  # TODO [X]: insert form data as a new Venue record in the db, instead
  error = False
  data = request.form
  db.session.begin()
  try:
    record: Venue = Venue(
      name = data['name'],\
      city = data['city'],\
      state = data['state'],\
      address = data['address'],\
      phone = data['phone'],\
      image_link = data['image_link'],\
      facebook_link = data['facebook_link'],\
      genres = data.getlist('genres'),\
      website_link = data['website_link'],\
      seeking_talent = data.get("seeking_talent", default=False, type=bool),\
      seeking_description = data['seeking_description']
    )
    db.session.add(record)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    
  except Exception as err:
    db.session.rollback()
    error = True
    print(sys.exc_info(), err)
    # TODO [X]: on unsuccessful db insert, flash an error instead.
    flash(f'An error occurred. Venue could not be listed.')
  
  finally:
    db.session.close()
    
  if error:
      abort(500)
  else:
    return render_template('pages/home.html') 
 

#  Edit Venue
#  ----------------------------------------------------------------
def edit_venue(venue_id):
  # TODO [X]: modify data to be the data object returned from db insertion
  form: VenueForm = VenueForm()
  venue: Venue =  Venue.query.get(venue_id);
  
  # TODO [X] : populate form with values from venue with ID <venue_id>  
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data =venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.image_link.data = venue.image_link
  form.facebook_link.data = venue.facebook_link
  form.genres.data = venue.genres
  form.website_link.data = venue.website_link
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.seeking_description
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)


def edit_venue_submission(venue_id):
  # TODO [X]: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  data = request.form
  record: Venue = Venue()
  db.session.begin()
  try:
    record: Venue = Venue.query.get(venue_id)
    record.name = data['name']
    record.city = data['city']
    record.state = data['state']
    record.address = data['address']
    record.phone = data['phone']
    record.image_link = data['image_link']
    record.facebook_link = data['facebook_link']
    record.genres = data.getlist('genres')
    record.website_link = data['website_link']
    record.seeking_talent = data.get("seeking_talent", default=False, type=bool)
    record.seeking_description = data['seeking_description']
    db.session.commit()
  
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    
  except Exception as err:
    db.session.rollback()
    print(sys.exc_info(), err)
    # TODO [X]: on unsuccessful db insert, flash an error instead.
    flash(f'An error occurred. Venue could not be listed.')
  
  finally:
    db.session.close()
    
  return redirect(url_for('show_venue', venue_id=venue_id))
