import json
import sys
from models import Availability, db, Show, Venue, Artist
from flask import abort, jsonify, make_response, render_template, request, Response, flash, redirect, url_for
from forms import ShowForm

#  Shows
#  ----------------------------------------------------------------

def shows():
  # displays list of shows at /shows
  # TODO [X] : replace with real venues data.
  data = Show.query.all()
  return render_template('pages/shows.html', shows=data)


def show_show(show_id):
   # TODO [X] : implemented show a show#
  try:
    data: Show = Show.query.get(show_id);
    if (data == None):
      raise Exception('Venue not found')
    return render_template('pages/show.html', show=data)
    
  except Exception as err:
    print(sys.exc_info(), err)
    # TODO [X]: on unsuccessful db insert, flash an error instead.
    flash(f'An error occurred.')
    abort(500)


def search_shows():
  # TODO [X]: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  qry = request.form.get('search_term', '')
  data = Show.query \
    .filter(
      Show.venue.has(Venue.name.ilike(f'%{qry}%')) |
      Show.artist.has(Artist.name.ilike(f'%{qry}%'))
     )\
    .all()
  response={
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_shows.html', results=response, search_term=request.form.get('search_term', ''))

def delete_show(show_id):
  raise Exception('Not implemented yet')

def autocomplete_artist():
  # .filter(Artist.name.ilike(f'{artist}%')) \
  #TODO [ ] eventually implement returning only the rows starting with the typed data
  rows = db.session.query(Artist) \
    .order_by(Artist.name) \
    .all()
  data = [row.as_autocomplete() for row in rows]
  
  response = make_response('response')
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.content_type='application/json'
  response.mimetype='application/json'
  response.data = json.dumps(data)
  response.status_code = 200
  
  return response
  #return 

def autocomplete_venue():
  #TODO [ ] eventually implement returning only the rows starting with the typed data
  rows = db.session.query(Venue) \
    .order_by(Venue.name) \
    .all()
  data = [row.as_autocomplete() for row in rows]
  
  response = make_response('response')
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.content_type='application/json'
  response.mimetype='application/json'
  response.data = json.dumps(data)
  response.status_code = 200
  
  return response

def get_availability(artist_id):
  try:
    data = Availability.query \
      .filter(Availability.artist_id == artist_id) \
      .order_by(Availability.created_at.desc()) \
      .limit(1) \
      .all()
    if len(data) == 0:
      return jsonify([])
    else:
      return jsonify([data[0].serialize()])
    
  except Exception as err:
    print(sys.exc_info(), err)
    # TODO [X]: on unsuccessful db insert, flash an error instead.
    flash(f'An error occurred.')
    return jsonify([])
  
def create_show_form():
  # renders form. do not touch.
  form: ShowForm = ShowForm()
  return render_template('forms/new_show.html', form=form)


def create_show_submission():
# TODO [X]: insert form data as a new Venue record in the db, instead
  error = False
  data = request.form
  try:
    db.session.begin()
    artist: Artist =  Artist.query.get(data['artist_id']);
    if (artist == None):
      raise Exception('Artist not found')
    
    record: Show = Show(
      venue_id = data['venue_id'],\
      artist_id = data['artist_id'],\
      start_time = data['start_time']
    )
    db.session.add(record)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show on ' + request.form['start_time'] + ' was successfully listed!')
    
  except Exception as err:
    db.session.rollback()
    error = True
    print(sys.exc_info(), err)
    # TODO [X]: on unsuccessful db insert, flash an error instead.
    flash(f'An error occurred. Show could not be listed.')
  
  finally:
    db.session.close()
    
  if error:
      abort(500)
  else:
    return redirect(url_for('index'))
