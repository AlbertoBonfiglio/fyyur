from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import (ARRAY, TIME)

db = SQLAlchemy()
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
# TODO [X]:  Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Venue(db.Model): # type: ignore
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, index=True)
    city = db.Column(db.String(120), nullable=False, index=True)
    state = db.Column(db.String(120),nullable=False, index=True)
    address = db.Column(db.String(120),nullable=False)
    phone = db.Column(db.String(36), nullable=False)
    
    image_link = db.Column(db.String(500),nullable=False, server_default='https://loremflickr.com/320/240/music,bar/all')
    facebook_link = db.Column(db.String(120))
    genres = db.Column(ARRAY(db.String(24)),nullable=False)
    website_link = db.Column(db.String(120),nullable=False)
    
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False, index=True)
    
    #relationships
    past_shows = db.relationship('Show', 
        order_by="Show.start_time",  
        primaryjoin ="and_(Show.venue_id==Venue.id, Show.start_time <= func.now()) ",
        viewonly=True
    )
    upcoming_shows = db.relationship('Show', 
        order_by="Show.start_time",  
        primaryjoin ="and_(Show.venue_id==Venue.id, Show.start_time > func.now()) ",
        viewonly=True
        )
        
    # Calculated    
    @hybrid_property
    def past_shows_count(self):
        return len(self.past_shows)
    
    @hybrid_property
    def upcoming_shows_count(self):
        return len(self.upcoming_shows)

    def __repr__(self):
        return f'<Venue ID: {self.id}, name: {self.name}, shows: {self.upcoming_shows}, past_shows: {self.past_shows}>'
      
    def as_autocomplete(self):
      return {'value': self.id, 'label': self.name}
    

class Artist(db.Model): # type: ignore
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, index=True)
    city = db.Column(db.String(120),nullable=False, index=True)
    state = db.Column(db.String(120),nullable=False, index=True)
    phone = db.Column(db.String(36), nullable=False)
    
    image_link = db.Column(db.String(500),nullable=False, server_default='https://loremflickr.com/320/240/band/all')
    facebook_link = db.Column(db.String(120))
    genres = db.Column(ARRAY(db.String(24)),nullable=False)
    website_link = db.Column(db.String(120), nullable=False)
    
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String, nullable=True)

    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False, index=True)
    
    #relationships
    availability = db.relationship('Availability', 
        order_by="desc(Availability.created_at)",  
        viewonly=True)

    past_shows = db.relationship('Show', 
        order_by="Show.start_time",  
        primaryjoin="and_(Show.artist_id==Artist.id, Show.start_time <= func.now()) ",
        viewonly=True
        )
    upcoming_shows = db.relationship('Show', 
        order_by="Show.start_time",  
        primaryjoin ="and_(Show.artist_id==Artist.id, Show.start_time > func.now()) ",
        viewonly=True
        ) 
    
    # Calculated
    @hybrid_property
    def past_shows_count(self):
        return len(self.past_shows)
    
    @hybrid_property
    def upcoming_shows_count(self):
        return len(self.upcoming_shows)
    
    @property
    def current_availability(self):
        if len(self.availability) > 0:
            return [self.availability[0]]
        else: 
            return self.availability
        
    
    def __repr__(self):
      return f'''< 
        Artist ID: {self.id}, 
        name: {self.name}, 
        shows: {self.upcoming_shows}, 
        past_shows: {self.past_shows},
        created: {self.created_at} 
      >'''
    
    def as_autocomplete(self):
      return {'value': self.id, 'label': self.name}
    
    def is_available(self, show_time):
      # Implement this if we want to validate show availability server-side
      # otherwise it's implemented in the UI
      raise Exception('Not implemented yet')
      return True

@dataclass
class Availability(db.Model): # type: ignore
    __tablename__ = 'Availability'
    id = db.Column(db.Integer, primary_key=True)
    artist_id= db.Column(db.Integer,db.ForeignKey('Artist.id'), index=True)
    start_time = db.Column(TIME, server_default=func.now(), nullable=False, index=True)
    end_time = db.Column(TIME, server_default=func.now(), nullable=False, index=True)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False, index=True)
    
    def serialize(self):
        return {
            'ID': self.id, 
            'artist_id': self.artist_id, 
            'start_time': self.start_time.isoformat(), 
            'end_time': self.end_time.isoformat(),
            'created_at': self.created_at.isoformat()
        }
    
    
class Show(db.Model): # type: ignore
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    venue_id= db.Column(db.Integer, db.ForeignKey('Venue.id'), index=True)
    artist_id= db.Column(db.Integer,db.ForeignKey('Artist.id'), index=True)
    venue = db.relationship('Venue')
    artist = db.relationship('Artist')
    start_time = db.Column(db.DateTime, server_default=func.now(), index=True)
    
    __table_args__ = (
        db.UniqueConstraint('venue_id', 'artist_id', 'start_time', name='venue_artist_time_idx' ),
    )