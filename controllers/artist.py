from models import db, Artist, Venue, Show
from flask import Flask, render_template,make_response, jsonify, request, Response, flash, redirect, url_for
from flask_wtf import Form
from forms import ArtistForm
from sqlalchemy.orm import load_only
from sqlalchemy import delete
#  Artists
#  ----------------------------------------------------------------
def artists():
  # TODO [X] : replace with real data returned from querying the database

  data = Artist.query.all();
  
  return render_template('pages/artists.html', artists=data)

def search_artists():
  # TODO [X]: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  qry = request.form.get('search_term', '')
  data = Artist.query.filter(Artist.name.ilike(f'%{qry}%')).all()
  response={
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO [X]: replace with real artist data from the artist table, using artist_id
  data = Artist.query.get(artist_id)
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))
#  Create Artist
#  ----------------------------------------------------------------

def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')

def delete_artist(artist_id):
  # TODO [X]: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  db.session.begin()
  response = make_response(
    jsonify({"redirect": url_for('index') }),
    200
  )
  try:
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