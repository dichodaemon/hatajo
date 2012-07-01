from hatajo import *
import random

def score( user_id, count ):
  min_date, max_date = db.session()\
      .query( db.func.min( db.Statistics.timestamp ),
              db.func.max( db.Statistics.timestamp ) )\
      .filter( db.Statistics.created == 1 )\
      .one()

  sold_z = db.session()\
      .query( db.func.sum( db.Statistics.sold ) )\
      .one()[0]

  view_z = db.session()\
      .query( db.func.sum( db.Statistics.view ) )\
      .filter( db.or_( db.Statistics.user_id == user_id, db.Statistics.user_id == None ) )\
      .one()[0]

  result = db.session()\
      .query( db.Product,
              db.func.sum( db.case( value = db.Statistics.user_id, whens = {user_id: 1.0 * db.Statistics.view / view_z, None: 1.0 * db.Statistics.view / view_z }, else_ = 0 ) ),
              db.func.sum( 1.0 * db.Statistics.sold / sold_z ),
              db.func.max( 1.0 * db.Statistics.created * ( db.Statistics.timestamp - min_date ) / ( max_date - min_date ) ),  
              db.func.min( db.case( value = db.Statistics.user_id, whens = {user_id: db.Statistics.sold * db.Statistics.created }, else_ = 0 ) ) )\
      .join( db.Statistics )\
      .group_by( db.Product.id )\
      .all()

  result = sorted( [[-( (0.7 + 0.25 * float( r[3] ) + 0.5 * random.random() ) * ( float( r[1] ) * 0.5 + float( r[2] ) * 0.5 ) ), r[0]] for r in result if r[4] == 0] )
  return [r[1] for r in result][:count]

