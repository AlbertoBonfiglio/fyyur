import sys
from models import db, Show, Venue, Artist
from flask import Flask, abort, render_template, request, Response, flash, redirect, url_for
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

def delete_show(show_id):
  raise Exception('Not implemented yet')


def create_show_form():
  # renders form. do not touch.
  languages = ["C++", "Python", "PHP", "Java", "C", "Ruby",
                     "R", "C#", "Dart", "Fortran", "Pascal", "Javascript"]
          
  
  
  form: ShowForm = ShowForm()
  return render_template('forms/new_show.html', form=form, languages=languages)

def create_show_submission():
# TODO [X]: insert form data as a new Venue record in the db, instead
  error = False
  data = request.form

  try:
    db.session.begin()
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
    return render_template('pages/home.html') 
