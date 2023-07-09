import sys
from flask import abort, flash, redirect, render_template, request, url_for
from forms import AvailabilityForm
from models import db, Availability


def create_availability_form(artist_id):
  form: AvailabilityForm = AvailabilityForm(artist_id=artist_id)
  return render_template('forms/create_availability.html', form=form)

def create_availability_submission(artist_id):
  # TODO [X]: insert form data as a new Venue record in the db, instead
  error = False
  data = request.form
  try:
    db.session.begin()
    # TODO [ ] Make sure start time is before end time
    record: Availability = Availability(
      artist_id = data['artist_id'],\
      start_time = data['start_time'],\
      end_time = data['end_time'],\
    )
    db.session.add(record)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist availability was successfully posted!')
    
  except Exception as err:
    db.session.rollback()
    error = True
    print(sys.exc_info(), err)
    # TODO [X]: on unsuccessful db insert, flash an error instead.
    flash(f'An error occurred. Availability could not be saved.')
  
  finally:
    db.session.close()
    
  if error:
      abort(500)
  else:
    url = url_for(f'artists')
    return redirect( f'{url}/{artist_id}' )
