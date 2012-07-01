import sys
import os

BASE_DIR = os.path.abspath( os.path.join( os.path.dirname( __file__ ), ".." ) )
path     = os.path.abspath( os.path.join( BASE_DIR, "python" ) )
if os.path.exists( path ):
  sys.path.append( path )

from hatajo import *
import ConfigParser
import codecs
import time
import random

#-------------------------------------------------------------------------------


config = ConfigParser.SafeConfigParser()
config.readfp( codecs.open( sys.argv[1], "r", "utf-8" ) )
db.create( config.get( "db", "url" ).strip( '"' ) )

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
    .filter( db.or_( db.Statistics.user_id == 2, db.Statistics.user_id == None ) )\
    .one()[0]

print min_date, max_date, view_z, sold_z

result = db.session()\
    .query( db.Product,
            db.func.sum( db.case( value = db.Statistics.user_id, whens = {2: 1.0 * db.Statistics.view / view_z, None: 1.0 * db.Statistics.view / view_z }, else_ = 0 ) ),
            db.func.sum( 1.0 * db.Statistics.sold / sold_z ),
            db.func.max( 1.0 * db.Statistics.created * ( db.Statistics.timestamp - min_date ) / ( max_date - min_date ) ),  
            db.func.min( db.case( value = db.Statistics.user_id, whens = {2: 0}, else_ = 1 ) ) )\
    .join( db.Statistics )\
    .group_by( db.Product.id )\
    .all()

for r in result:
  print r

result = sorted( [[-( float( r[1] ) * 0.4 + float( r[2] ) * 0.3 + float( r[3] ) * 0.2 + random.random() * 0.1 ), r[4], r[0]] for r in result if r[4] == 1] )

for r in result:
  print r

