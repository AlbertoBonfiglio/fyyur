from models import db, Venue, Artist, Show
from sqlalchemyseeder import ResolvingSeeder
from sqlalchemy.sql import func

def seed(): 
  _count=0
  try:
    db.session.expire_all()
    venues = db.session.query(func.count(Venue.id)).scalar()
    if venues < 1 :
      print(f'Found no venues. Seeding....')
      seeder = ResolvingSeeder(db.session)
      seeder.register_class(Venue)
      seeder.register_class(Artist)
      seeder.register_class(Show)

      print(f'Seeding {_count} entities...')
      # See API reference for more options
      new_entities = seeder.load_entities_from_json_file('./seed.json', separate_by_class=True, flush_on_create=True, commit=False)
      _count = len(new_entities)
      
      
      #resetting the counters 
      print(f'Seeding {_count} entities...')
      artist_counter = 'ALTER SEQUENCE public."Artist_id_seq" RESTART WITH 100'
      venue_counter = 'ALTER SEQUENCE public."Venue_id_seq" RESTART WITH 100'
      show_counter = 'ALTER SEQUENCE public."Show_id_seq" RESTART WITH 100'
      
      db.session.execute(artist_counter)
      db.session.execute(venue_counter)
      db.session.execute(show_counter)
      
      db.session.commit()
    else:  
      print(f'Found {venues} venues.')
      
  except Exception as ex:
    print(ex)
    db.session.rollback  
    
  finally:
    print(f'Seeding complete. {_count} Entities inserted.')
    