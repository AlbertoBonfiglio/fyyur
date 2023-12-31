from flask import Flask, render_template
import controllers.main as mc
import controllers.venue as vc
import controllers.artist as ac
import controllers.show as sc
import controllers.availability as avc

def config_routes(app) :
  # @app.route('/', methods=["POST", "GET", "DELETE"])
  
  @app.errorhandler(404)
  def not_found_error(error):
    return render_template('errors/404.html'), 404

  @app.errorhandler(500)
  def server_error(error):
    return render_template('errors/500.html'), 500

  #----------------------------------------------------------------------------#
  # Index Routes.
  #----------------------------------------------------------------------------#
  app.add_url_rule('/', view_func=mc.index)
  
  #----------------------------------------------------------------------------#
  # Venue Routes.
  #----------------------------------------------------------------------------#
  app.add_url_rule('/venues', view_func=vc.venues)
  app.add_url_rule('/venues/search',view_func=vc.search_venues,  methods=['POST'])
  app.add_url_rule('/venues/<int:venue_id>', view_func=vc.show_venue)
  #app.add_url_rule('/venues/create', view_func=vc.create_venue_form, methods=['GET'])
  app.add_url_rule('/venues/create', view_func=vc.create_venue_submission, methods=['GET'])
  app.add_url_rule('/venues/create', view_func=vc.create_venue_submission, methods=['POST'])
  #app.add_url_rule('/venues/<int:venue_id>/edit', view_func=vc.edit_venue, methods=['GET'])
  app.add_url_rule('/venues/<int:venue_id>/edit', view_func=vc.edit_venue_submission, methods=['GET'])
  app.add_url_rule('/venues/<int:venue_id>/edit', view_func=vc.edit_venue_submission, methods=['POST'])
  app.add_url_rule('/venues/<venue_id>', view_func=vc.delete_venue, methods=['DELETE'])

  #----------------------------------------------------------------------------#
  # Artist Routes.
  #----------------------------------------------------------------------------#
  app.add_url_rule('/artists', view_func=ac.artists)
  app.add_url_rule('/artists/search',view_func=ac.search_artists,  methods=['POST'])
  app.add_url_rule('/artists/<int:artist_id>', view_func=ac.show_artist)
  app.add_url_rule('/artists/create', view_func=ac.create_artist_submission, methods=['GET'])
  app.add_url_rule('/artists/create', view_func=ac.create_artist_submission, methods=['POST'])
  app.add_url_rule('/artists/<int:artist_id>/edit', view_func=ac.edit_artist_submission, methods=['GET'])
  app.add_url_rule('/artists/<int:artist_id>/edit', view_func=ac.edit_artist_submission, methods=['POST'])
  app.add_url_rule('/artists/<artist_id>', view_func=ac.delete_artist, methods=['DELETE'])
  app.add_url_rule('/artists/<artist_id>/availability', view_func=avc.create_availability_form, methods=['GET'])
  app.add_url_rule('/artists/<artist_id>/availability', view_func=avc.create_availability_submission, methods=['POST'])

  #----------------------------------------------------------------------------#
  # Show Routes
  #----------------------------------------------------------------------------#
  app.add_url_rule('/shows', view_func=sc.shows)
  app.add_url_rule('/shows/<int:show_id>', view_func=sc.show_show)
  app.add_url_rule('/shows/search',view_func=sc.search_shows,  methods=['POST'])
  app.add_url_rule('/shows/create', view_func=sc.create_show_form, methods=['GET'])
  app.add_url_rule('/shows/create', view_func=sc.create_show_submission, methods=['POST'])
  #app.add_url_rule('/shows/<int:show_id>/edit', view_func=sc.show_show, methods=['GET'])
  #app.add_url_rule('/shows/<int:show_id>/edit', view_func=sc.show_show, methods=['POST'])
  app.add_url_rule('/shows/<show_id>', view_func=sc.delete_show, methods=['DELETE'])
  app.add_url_rule('/shows/create/autocomplete_artist', view_func=sc.autocomplete_artist, methods=['GET'])
  app.add_url_rule('/shows/create/autocomplete_venue', view_func=sc.autocomplete_venue, methods=['GET'])
  app.add_url_rule('/shows/create/get_availability/<artist_id>', view_func=sc.get_availability, methods=['GET'])
