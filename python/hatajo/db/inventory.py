# -*- coding: utf-8 -*-

from __global import *

class Inventory( Base ):
  __tablename__ = 'inventory'

  id         = Column( Integer, primary_key = True )
  product_id = Column( Integer, ForeignKey( "products.id" ), index = True )
  date       = Column( DateTime )
  normal_price     = Column( Float )
  discounted_price = Column( Float )
  units            = Column( Integer )
  note             = Column( String )

  product = relation( 
    "Product", 
    uselist = False, 
    backref = backref( "inventory", cascade = "all,delete-orphan" ) 
  )
  
  def __init__( self ):
    self.units = 0
    self.normal_price = 0
    self.discounted_price = 0
    self.note = ""

