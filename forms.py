from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, HiddenField
from wtforms.validators import DataRequired, AnyOf, URL
from enums import GenreEnum, StateEnum

# TODO [X] implement validation logic for state
# TODO [X] implement enum restriction
        
class ShowForm(FlaskForm):
    artist_id = HiddenField(
        'artist_id',
        validators=[DataRequired()],
    )
    artist_name = StringField(
        'artist_name',
        validators=[DataRequired()],
    )
    venue_id = HiddenField(
        'venue_id',
        validators=[DataRequired()],
    )
    venue_name = StringField(
        'venue_name',
        validators=[DataRequired()],
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )

class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices= StateEnum.choices()
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link', validators=[DataRequired(), URL()],
        default='https://loremflickr.com/320/240/music,bar/all'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices = GenreEnum.choices(),
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website_link = StringField(
        'website_link',
        validators=[URL()]
    )

    seeking_talent = BooleanField(
        'seeking_talent', 
        default=False, 
        false_values=('False', 'false', '')
    )

    seeking_description = StringField(
        'seeking_description'
    )


class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices= StateEnum.choices()
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link', validators=[DataRequired(), URL()],
        default='https://loremflickr.com/320/240/band/all'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices= GenreEnum.choices()
     )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
     )
    website_link = StringField(
        'website_link',
        validators=[URL()]
     )
    seeking_venue = BooleanField(
        'seeking_venue', 
        default=False, 
        false_values=('False', 'false', '')
    )
    seeking_description = StringField(
            'seeking_description'
     )
