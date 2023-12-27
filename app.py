#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import sys
import json
from unittest import result
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import config


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__, template_folder='templates', static_folder='static')
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.init_app(app)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
from model import *

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
 data=[{
    "city": "Surulere",
    "state": "Lagos",
    "venues": [{
      "id": 1,
      "name": "Landmark Event",
      "num_upcoming_shows": 0,
    }, {
      "id": 3,
      "name": "Jane's Coffee",
      "num_upcoming_shows": 1,
    }]
  }, {
    "city": "Victoria Island",
    "state": "Lagos",
    "venues": [{
      "id": 2,
      "name": "Fresh Bar",
      "num_upcoming_shows": 0,
    }]
  }]
 newData = []
 location = Venue.query.distinct(Venue.city, Venue.state).all()
 for items in location:
    venues = Venue.query.filter_by(city=location.city, state=location.city).all()

    venue_new= []
    for venue in venues:
      venue_new.append({'id':venue.id, 'name': venue.name})
    
    venues_id = {'city':location.city, 'state':location.state}
    venues_id['venues'] = venue_new
    newData.append(venues_id)
 
    return render_template('pages/venues.html', areas=newData);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  search_term = request.form.get('search_term', '')
  search_result = Venue.query.filterby(Venue.name.ilike(f'%{search_term}%'))
  
  response={
    "count": result.count(),
    "data": result
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
   data1={
    "id": 1,
    "name": "Landmark Event",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "10 Queen Street",
    "city": "Surulere",
    "state": "Lagos",
    "phone": "080-222-2222",
    "website": "https://www.landmark Event.com",
    "facebook_link": "https://www.facebook.com/landmarkevent",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://unsplash.com/photos/ZGa9d1a_4tA",
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Helen Paul",
      "artist_image_link": "https://unsplash.com/photos/JXUfF7HYfMo",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
   }
   data2={
    "id": 2, 
    "name": "Fresh bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "33 Ozumba Street",
    "city": "Victoria Island",
    "state": "Lagos",
    "phone": "080-333-3333",
    "website": "https://www.freshbar.com",
    "facebook_link": "https://www.facebook.com/freshbar",
    "seeking_talent": False,
    "image_link": "https://unsplash.com/photos/JXUfF7HYfMo",
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
   }
   data3={
    "id": 3,
    "name": "Jane's Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "10 Queen Street",
    "city": "Ikeja",
    "state": "Lagos",
    "phone": "080-324-5555",
    "website": "https://www.Janescoffee.com",
    "facebook_link": "https://www.facebook.com/Jane's Coffee",
    "seeking_talent": False,
    "image_link": "https://unsplash.com/photos/HvZDCuRnSaY",
    "past_shows": [{
      "artist_id": 5,
      "artist_name": "Mcjob Peters",
      "artist_image_link": "https://unsplash.com/photos/4Yv84VgQkRM",
      "start_time": "2019-06-15T23:00:00.000Z"
     }],
    "upcoming_shows": [{
      "artist_id": 6,
      "artist_name": "Tom Coker",
      "artist_image_link": "https://unsplash.com/photos/ZXfUUM_LR0k",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "Tom Coker",
      "artist_image_link": "https://unsplash.com/photos/ZXfUUM_LR0k",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "Tom Coker",
      "artist_image_link": "https://unsplash.com/photos/ZXfUUM_LR0k",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 1,
    "upcoming_shows_count": 1,
   }
   data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
   return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  try: 
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    website = request.form['website']
    seeking_talent = True if 'seeking_talent' in request.form else False 
    seeking_description = request.form['seeking_description']

    db.session.add(venues)
    db.session.commit()
  except: 
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally: 
    db.session.close()
  if error: 
    flash('An error occurred. Venue ' + request.form['name']+ ' could not be listed.')
  else: 
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
  if error: 
    flash(f'An error occurred' + 'Venue {venue_id}' + 'could not be deleted.')
  else:
    flash(f'Venue' + '{venue_id}' + 'was successfully deleted.')
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
   data=[{
    "id": 4,
    "name": "Helen Paul",
  }, {
    "id": 5,
    "name": "Mcjob Peters",
  }, {
    "id": 6,
    "name": "Tom Coker",
  }]
   newData = []
   artists = db.session.query(Artist.id, Artist.name).all()

   return render_template('pages/artists.html', artists=newData)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  search_result = artists.query.filterby(Artist.name.ilike(f'%{search_term}%'))

  response={
    "count": result.count (),
    "data": result
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
   data1={
    "id": 4,
    "name": "Helen Paul",
    "genres": ["Rock n Roll"],
    "city": "Surulere",
    "state": "Lagos",
    "phone": "080-123-5000",
    "website": "https://www.helenpaul.com",
    "facebook_link": "https://www.facebook.com/helenpaul",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in Lagos!",
    "image_link": "https://unsplash.com/photos/JXUfF7HYfMo",
    "past_shows": [{
      "venue_id": 1,
      "venue_name": "Landmark Event",
      "venue_image_link": "https://unsplash.com/photos/ZXfUUM_LR0k+",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
   }
   data2={
    "id": 5,
    "name": "Mcjob Peters",
    "genres": ["Jazz"],
    "city": "Ikeja",
    "state": "Lagos",
    "phone": "080-400-5000",
    "facebook_link": "https://www.facebook.com/mcjobpeters",
    "seeking_venue": False,
    "image_link": "https://unsplash.com/photos/4Yv84VgQkRM",
    "past_shows": [{
      "venue_id": 3,
      "venue_name": "Jane's Coffee",
      "venue_image_link": "https://unsplash.com/photos/HvZDCuRnSaY",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
   }
   data3={
    "id": 6,
    "name": "Tom Coker",
    "genres": ["Jazz", "Classical"],
    "city": "Ikeja",
    "state": "Lagos",
    "phone": "080-325-5432",
    "seeking_venue": False,
    "image_link": "https://unsplash.com/photos/ZXfUUM_LR0k",
    "past_shows": [],
    "upcoming_shows": [{
      "venue_id": 3,
      "venue_name": "Jane's Coffee",
      "venue_image_link": "https://unsplash.com/photos/HvZDCuRnSaY",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Jane's Coffee",
      "venue_image_link": "https://unsplash.com/photos/HvZDCuRnSaY",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Jane's Coffee",
      "venue_image_link": "https://unsplash.com/photos/HvZDCuRnSaY",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 0,
    "upcoming_shows_count": 3,
  }
   data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
   return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  artist={
    "id": 4,
    "name": "Helen ",
    "genres": ["Rock n Roll"],
    "city": "Surulere",
    "state": "Lagos",
    "phone": "080-123-5000",
    "website": "https://www.helenpaul.com",
    "facebook_link": "https://www.facebook.com/helenpaul",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the Surulere!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
   }
  if artist: 
     id= artist.id
     name = artist.name
     genres= artist.genres
     city= artist.city
     state= artist.state
     phone= artist.phone
     website= artist.website
     facebook_link= artist.facebook_link
     seeking_venue= artist.seeking_venue
     seeking_description= artist.seeking_description
     image_link= artist.image_link
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
   error = False  
   artist = Artist.query.get(artist_id)
   
   try: 
    form= ArtistForm
    artist.name = request.form['name']
    artist.genres = request.form.getlist('genres')
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.website = request.form['website']
    artist.facebook_link = request.form['facebook_link']
    artist.seeking_venue = request.venue['seeking_venue']
    artist.seeking_description = request.form['seeking_description']
    artist.image_link = request.form['image_link']
    
    db.session.commit()
   except: 
    db.session.rollback()
    error = True
    print(sys.exc_info()) 
   finally: 
    db.session.close()   
   if error: 
    flash('An error occurred' + 'update unsuccessful.')
   else: 
    flash('Artist was successfully updated!')
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  venue={
    "id": 1,
    "name": "Landmark event",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "10 Queen Street",
    "city": "Surulere",
    "state": "Lagos",
    "phone": "080-222-2222",
    "website": "https://www.Landmarkevent.com",
    "facebook_link": "https://www.facebook.com/Landmarkevent",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  if venue: 
    id = venue.id
    name = venue.name
    genres = venue.genres
    address = venue.address
    city = venue.city
    state = venue.state
    phone = venue.phone
    website_link = venue.website
    facebook_link = venue.facebook_link
    seeking_talent = venue.seeking_talent
    seeking_description = venue.seeking_description
    image_link = venue.image_link
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False  
  venue = Venue.query.get(venue_id)

  try: 
    form = VenueForm
    venue.name = request.form['name']
    venue.genres = request.form.getlist('genres')
    venue.address = request.form['address']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.phone = request.form['phone']
    venue.website = request.form['website']
    venue.facebook_link = request.form['facebook_link']
    venue.seeking_talent = True if 'seeking_talent' in request.form else False 
    venue.seeking_description = request.form['seeking_description']
    venue.image_link = request.form['image_link']

    db.session.commit()
  except: 
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally: 
    db.session.close()
  if error: 
    flash(f'An error occurred' + 'update unsuccessful')
  else: 
    flash(f'Venue was successfully updated!')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
 error = False

 try: 
    name = request.form['name']
    genres = request.form.getlist('genres')
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    website = request.form['website']
    facebook_link = request.form['facebook_link']
    seeking_venue = True if 'seeking_venue' in request.form else False
    seeking_description = request.form['seeking_description']
    image_link = request.form['image_link']

    artist = Artist(name=name, genres=genres, city=city, state=state, phone=phone, website=website, facebook_link=facebook_link, seeking_venue=seeking_venue, seeking_description=seeking_description, image_link=image_link)
    db.session.add(artist)
    db.session.commit()
 except: 
    db.session.rollback()
    error = True
    print(sys.exc_info())
 finally: 
    db.session.close()
 if error: 
    flash('An error occurred. Artist ' + request.form['name']+ ' could not be listed.')
 if not error: 
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
 return render_template('pages/home.html')
  # on successful db insert, flash success 
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')



#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data=[{
    "venue_id": 1,
    "venue_name": "Landmark Events",
    "artist_id": 4,
    "artist_name": "Helen Paul",
    "artist_image_link": "https://unsplash.com/photos/JXUfF7HYfMo",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Jane's Coffee",
    "artist_id": 5,
    "artist_name": "Mcjob Peters",
    "artist_image_link": "https://unsplash.com/photos/4Yv84VgQkRM",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Jane's Coffee",
    "artist_id": 6,
    "artist_name": "Tom Coker",
    "artist_image_link": "https://unsplash.com/photos/ZXfUUM_LR0k",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Jane's Coffee",
    "artist_id": 6,
    "artist_name": "Tom Coker",
    "artist_image_link": "https://unsplash.com/photos/ZXfUUM_LR0k",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Jane's Coffee",
    "artist_id": 6,
    "artist_name": "Tom Coker",
    "artist_image_link": "https://unsplash.com/photos/ZXfUUM_LR0k",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
  newData = []
  shows= Show.query.all()
  for data in shows:
    data.append({
      'venue_id': data.venue_id,
      'venue_name': data.venue.name,
      'artist_id': data.artist_id,
      'artist_name': data.artist.name,
      'artist_image_link': data.artist.image_link,
      'start_time': format_datetime(str(data.start_time))
    })  
  return render_template('pages/shows.html', shows=newData)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
   error = False
   try:
    show = Show
    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']

    db.session.add(show)
    db.session.commit()
   except: 
    db.session.rollback()
    error = True
    print(sys.exc_info())
   finally: 
    db.session.close()
   if error: 
    flash('An error occurred'+'update unsuccessful')
   else: 
    flash('Show was successfully listed')
   return render_template('pages/home.html') 
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__': 
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
