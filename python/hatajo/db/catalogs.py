# -*- coding: utf-8 -*-

from __global import *

class Catalogs( Base ):
  __tablename__ = 'catalogs'
  id           = Column( Integer, primary_key = True )
  catalog_name = Column( String )
  value        = Column( String )

  byId   = classmethod( byId )

  def __init__( self, catalog_name, value ):
    self.catalog_name = catalog_name
    self.value        = value

