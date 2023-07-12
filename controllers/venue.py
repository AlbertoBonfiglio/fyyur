from datetime import datetime
from models import db, Venue, Show
from flask import render_template, request,jsonify, make_response, flash, redirect, url_for, abort
from forms import VenueForm
from sqlalchemy import delete
import sys

def venues():
  # TODO [X]: replace with real venues data.
  # Aggregate by state and city
  # num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  try:
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
  except Exception as err:
    print(sys.exc_info(), err)
    # TODO [X]: on unsuccessful db insert, flash an error instead.
    flash(f'An error occurred.')
    abort(500)
  
def search_venues():
  # TODO [X]: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  try:
    qry = request.form.get('search_term', '')
    data = Venue.query.filter(Venue.name.ilike(f'%{qry}%')).all()
    response={
      "count": len(data),
      "data": data
    }

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))
  except Exception as err:
    print(sys.exc_info(), err)
    # TODO [X]: on unsuccessful db insert, flash an error instead.
    flash(f'An error occurred.')
    abort(500)
  

def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO [X] : replace with real venue data from the venues table, using venue_id #
  try:
    data: Venue = Venue.query.get(venue_id);
    if (data == None):
      raise Exception('Venue not found')

    past_shows_query = Show.query.join(Venue) \
      .filter(Show.venue_id==venue_id) \
      .filter(Show.start_time<datetime.now()) \
      .all()   
      
    future_shows_query = Show.query.join(Venue) \
      .filter(Show.venue_id==venue_id) \
      .filter(Show.start_time>=datetime.now()) \
      .all()   
    
    return render_template('pages/show_venue.html', venue=data, future_shows= future_shows_query, past_shows=past_shows_query)
    
  except Exception as err:
    print(sys.exc_info(), err)
    # TODO [X]: on unsuccessful db insert, flash an error instead.
    flash(f'An error occurred.')
    abort(500)
  

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
def create_venue_submission():
  # TODO [X]: insert form data as a new Venue record in the db, instead
  error = False
  form: VenueForm = VenueForm(request.form)
  try:
    db.session.begin()
    if (request.method == 'POST'):
      if (form.validate_on_submit() == False):
        return render_template('forms/new_venue.html', form=form)
    
      record: Venue = Venue(
        name = form.name.data,
        city = form.city.data,
        state = form.state.data,
        address = form.address.data,
        phone = form.phone.data,
        image_link = form.image_link.data,
        facebook_link = form.facebook_link.data,
        genres = form.genres.data ,
        website_link = form.website_link.data,
        seeking_talent = form.seeking_talent.data,
        seeking_description = form.seeking_description.data ,
      )
      db.session.add(record)
      db.session.commit()
      # on successful db insert, flash success
      flash('Venue ' + record.name + ' was successfully listed!')
      
    else: # method=GET
      return render_template('forms/new_venue.html', form=form)
    
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
    return redirect(url_for('index')) 
 

#  Edit Venue
#  ----------------------------------------------------------------
def edit_venue_submission(venue_id):
  # TODO [X]: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  try:
    form: VenueForm = VenueForm(request.form)
    db.session.begin()
    venue: Venue = Venue.query.get(venue_id)
    if (venue == None):
      raise Exception('Venue not found')
    
    if (request.method == 'POST'):
      if (form.validate_on_submit() == False):
        return render_template('forms/edit_venue.html', form=form, venue_id=venue_id)
  
      venue.name = form.name.data
      venue.city = form.city.data
      venue.state = form.state.data
      venue.address = form.address.data
      venue.phone = form.phone.data
      venue.image_link = form.image_link.data
      venue.facebook_link = form.facebook_link.data
      venue.genres = form.genres.data
      venue.website_link = form.website_link.data
      venue.seeking_talent = request.form.get("seeking_talent", default=False, type=bool) # form.seeking_talent.data,
      venue.seeking_description = form.seeking_description.data
      db.session.commit()
  
      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully updated!')
    
    else:
      # TODO [X] : populate form with values from venue with ID 
      form.name.data = venue.name
      form.city.data = venue.city
      form.state.data =venue.state
      form.address.data = venue.address
      form.phone.data = venue.phone
      form.image_link.data = venue.image_link
      form.facebook_link.data = venue.facebook_link
      form.genres.data = venue.genres
      form.website_link.data = venue.website_link
      form.seeking_talent.data  = venue.seeking_talent
      form.seeking_description.data = venue.seeking_description 
      return render_template('forms/edit_venue.html', form=form, venue_id=venue_id)
    
  except Exception as err:
    db.session.rollback()
    print(sys.exc_info(), err)
    # TODO [X]: on unsuccessful db insert, flash an error instead.
    flash(f'An error occurred. Venue could not be updated.')
  
  finally:
    db.session.close()
    
  return redirect(url_for('show_venue', venue_id=venue_id))
