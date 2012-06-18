# -*- coding: utf-8 -*-

from __global import *

class Review( Base ):
  __tablename__ = 'reviews'
  id         = Column( Integer, primary_key = True )
  product_id = Column( Integer, ForeignKey( "products.id" ) )
  name       = Column( String )
  alias      = Column( String )
  date       = Column( Date )
  rating     = Column( Float )
  content    = Column( String )

  by_id = classmethod( by_id )
  
  product = relation( 
    "Product", 
    uselist = False, 
    backref = backref( "reviews", cascade = "all,delete-orphan" )
  )
