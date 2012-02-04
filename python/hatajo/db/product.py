# -*- coding: utf-8 -*-

from __global import *
from catalog_entry import CatalogEntry

class Product( Base ):
  __tablename__ = 'products'
  id        = Column( Integer, primary_key = True )
  name      = Column( String )

  by_id   = classmethod( by_id )

  def __init__( self, name ):
    self.name  = catalog_name


ProductGenre = Table( "product_genre", metadata,
  Column( "product_id", Integer, ForeignKey( Product.id ) ),
  Column( "genre_id", Integer, ForeignKey( CatalogEntry.id ) )
)

Product.genres = relation( CatalogEntry, secondary = ProductGenre )

ProductActor = Table( "product_actor", metadata,
  Column( "product_id", Integer, ForeignKey( Product.id ) ),
  Column( "actor_id", Integer, ForeignKey( CatalogEntry.id ) )
)

Product.actors = relation( CatalogEntry, secondary = ProductActor )

ProductDirector = Table( "product_director", metadata,
  Column( "product_id", Integer, ForeignKey( Product.id ) ),
  Column( "director_id", Integer, ForeignKey( CatalogEntry.id ) )
)

Product.directors = relation( CatalogEntry, secondary = ProductDirector )

