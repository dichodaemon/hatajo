# -*- coding: utf-8 -*-

from __global import *

class CatalogEntry( Base ):
  __tablename__ = 'catalog_entries'
  id           = Column( Integer, primary_key = True )
  catalog_name = Column( String )
  value        = Column( String )

  by_id   = classmethod( by_id )

  def __init__( self, catalog_name, value ):
    self.catalog_name = catalog_name
    self.value        = value

