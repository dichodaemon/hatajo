# -*- coding: utf-8 -*-

from __global import *

class Statistics( Base ):
  __tablename__ = "statistics"
  id = Column( Integer, primary_key = True )
  user_id    = Column( Integer, ForeignKey( "users.id" ), index = True )
  product_id = Column( Integer, ForeignKey( "products.id" ), index = True )
  timestamp  = Column( Float )
  view       = Column( Integer, default = 0 )
  sold       = Column( Integer, default = 0 )
  created    = Column( Integer, default = 0 )

  user = relation( "User", uselist = False )
  product = relation( "Product", uselist = False )

