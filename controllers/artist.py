from datetime import datetime
from models import  Venue, db, Artist, Show
from flask import abort, render_template,make_response, jsonify, request, flash, redirect, url_for
from forms import ArtistForm
from sqlalchemy import delete
import sys

#  Artists
#  ----------------------------------------------------------------
def artists():
  # TODO [X] : replace with real data returned from querying the database
  try:
    data = Artist.query.all();
    return render_template('pages/artists.html', artists=data)
  except Exception as err:
    print(sys.exc_info(), err)
    # TODO [X]: on unsuccessful db insert, flash an error instead.
    flash(f'An error occurred.')
    abort(500)
  

def search_artists():
  # TODO [X]: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  try:
    qry = request.form.get('search_term', '')
    data = Artist.query.filter(Artist.name.ilike(f'%{qry}%')).all()
    response={
      "count": len(data),
      "data": data
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))
  except Exception as err:
    print(sys.exc_info(), err)
    # TODO [X]: on unsuccessful db insert, flash an error instead.
    flash(f'An error occurred.')
    abort(500)
  
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO [X]: replace with real artist data from the artist table, using artist_id
  try:
    artist: Artist = Artist.query.get(artist_id)
    past_shows_query = Show.query.join(Venue) \
      .filter(Show.artist_id==artist_id) \
      .filter(Show.start_time<datetime.now()) \
      .all()   
      
    future_shows_query = Show.query.join(Venue) \
      .filter(Show.artist_id==artist_id) \
      .filter(Show.start_time>=datetime.now()) \
      .all()   
    
    if (artist == None):
      raise Exception('Artist not found')
    return render_template('pages/show_artist.html', artist=artist, past_shows=past_shows_query, future_shows=future_shows_query)
  
  except Exception as err:
    print(sys.exc_info(), err)
    # TODO [X]: on unsuccessful db insert, flash an error instead.
    flash(f'An error occurred. Artist could not be found.')
    abort(500)
  

def delete_artist(artist_id):
  # TODO [X]: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  response = make_response(
    jsonify({"redirect": url_for('index') }),
    200
  )
  try:
    db.session.begin()
    m2m = delete(Show).where(Show.artist_id == artist_id)
    qry = delete(Artist).where(Artist.id == artist_id)

    db.session.execute(m2m)
    db.session.execute(qry)
    db.session.commit()
    
    flash(f'Artist {artist_id} deleted.')    
  except Exception as err:
    flash(f'An error occurred. Artist {artist_id} could not be deleted.')
    response = make_response(
      jsonify({"err": getattr(err, 'message', repr(err)) }),
      500
    )
    db.session.rollback()
  finally:
    db.session.close()
  
  response.headers["Content-Type"] = "application/json"  
  return response
  

#  Create Artist
#  ----------------------------------------------------------------
def create_artist_submission():
  # TODO [X]: insert form data as a new Venue record in the db, instead
  error = False
  form: ArtistForm = ArtistForm(request.form)
  try:
    db.session.begin()
    if (request.method == 'POST'):
      if (form.validate_on_submit() == False):
        return render_template('forms/new_artist.html', form=form)

      record: Artist = Artist(
        name = form.name.data,
        city = form.city.data,
        state = form.state.data,
        phone = form.phone.data,
        image_link = form.image_link.data,
        facebook_link = form.facebook_link.data,
        genres = form.genres.data ,
        website_link = form.website_link.data,
        seeking_venue = form.seeking_venue.data,
        seeking_description = form.seeking_description.data ,
      )
      db.session.add(record)
      db.session.commit()
      # on successful db insert, flash success
      flash('Artist ' + record.name + ' was successfully listed!')

    else: # method=GET
      return render_template('forms/new_artist.html', form=form)
    
  except Exception as err:
    db.session.rollback()
    error = True
    print(sys.exc_info(), err)
    # TODO [X]: on unsuccessful db insert, flash an error instead.
    flash(f'An error occurred. Artist could not be listed.')
  
  finally:
    db.session.close()
    
  if error:
      abort(500)
  else:
    return redirect(url_for('index')) 

  
#  Update
#  ----------------------------------------------------------------
def edit_artist_submission(artist_id):
  # TODO [X]: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  try:
    form:ArtistForm = ArtistForm(request.form)
    db.session.begin()
    artist: Artist = Artist.query.get(artist_id)
    if (artist == None):
      raise Exception('Artist not found')

    if (request.method == 'POST'):
      if (form.validate_on_submit() == False):
        return render_template('forms/edit_artist.html', form=form, artist_id=artist_id)
   
      artist.name = form.name.data
      artist.city = form.city.data
      artist.state = form.state.data
      artist.phone = form.phone.data
      artist.image_link = form.image_link.data
      artist.facebook_link = form.facebook_link.data
      artist.genres = form.genres.data #  form.getlist('genres')
      artist.website_link = form.website_link.data
      artist.seeking_venue = form.seeking_venue.data # .get("seeking_venue", default=False, type=bool)
      artist.seeking_description = form.seeking_description.data
      db.session.commit()

      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully update!')
    else:
      # TODO [X] : populate form with values from venue with ID 
      form.name.data = artist.name
      form.city.data = artist.city
      form.state.data =artist.state
      form.phone.data = artist.phone
      form.image_link.data = artist.image_link
      form.facebook_link.data = artist.facebook_link
      form.genres.data = artist.genres
      form.website_link.data = artist.website_link
      form.seeking_venue.data  = artist.seeking_venue
      form.seeking_description.data = artist.seeking_description 
      return render_template('forms/edit_artist.html', form=form, artist_id=artist_id)
     
  except Exception as err:
    db.session.rollback()
    print(sys.exc_info(), err)
    # TODO [X]: on unsuccessful db insert, flash an error instead.
    flash(f'An error occurred. Artist could not be updated.')
  
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))
