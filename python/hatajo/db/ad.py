# -*- coding: utf-8 -*-

from __global import *

class Ad( Base ):
  __tablename__ = 'ads'
  id          = Column( Integer, primary_key = True )
  name        = Column( String )
  enabled     = Column( Boolean )
  ad_type_id  = Column( Integer, ForeignKey( "catalog_entries.id" ) )
  content     = Column( String )
  valid_until = Column( Date )

  by_id   = classmethod( by_id )

  ad_type = relation( "CatalogEntry", uselist = False )

