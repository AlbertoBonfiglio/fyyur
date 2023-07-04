import sys
from models import db, Show, Venue, Artist
from flask import Flask, abort, render_template, request, Response, flash, redirect, url_for
from flask_wtf import Form
from forms import ShowForm

def index():
  new_artists = Artist.query.order_by(Artist.created_at.desc()).limit(10).all() 
  new_venues = Venue.query.order_by(Venue.created_at.desc()).limit(10).all() 
  new_shows = Show.query.order_by(Show.start_time.desc()).limit(10).all() 
  return render_template('pages/home.html', artists=new_artists, venues=new_venues, shows=new_shows )
