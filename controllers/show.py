from models import db, Show, Venue, Artist
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_wtf import Form
from forms import ShowForm

#  Shows
#  ----------------------------------------------------------------

def shows():
  # displays list of shows at /shows
  # TODO [X] : replace with real venues data.
  data = Show.query.all()
  return render_template('pages/shows.html', shows=data)


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

def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

def delete_show(show_id):
  raise Exception('Not implemented yet')