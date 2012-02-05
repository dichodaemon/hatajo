# -*- coding: utf-8 -*-

from __global import *
from catalog_entry import CatalogEntry

class Product( Base ):
  __tablename__ = 'products'
  id         = Column( Integer, primary_key = True )
  name       = Column( String )
  format_id  = Column( Integer, ForeignKey( "catalog_entries.id" ) )
  region_id  = Column( Integer, ForeignKey( "catalog_entries.id" ) )
  item_count = Column( Integer )
  age_rating_id = Column( Integer, ForeignKey( "catalog_entries.id" ) )
  studio_id     = Column( Integer, ForeignKey( "catalog_entries.id" ) )
  media_id      = Column( Integer, ForeignKey( "catalog_entries.id" ) )
  duration   = Column( String )
  rtc        = Column( String )
  bar_code   = Column( String )
  special_features = Column( String )
  summary          = Column( String )



  format = relation( "CatalogEntry", uselist = False, primaryjoin = "Product.format_id == CatalogEntry.id" )
  region = relation( "CatalogEntry", uselist = False, primaryjoin = "Product.region_id == CatalogEntry.id" )
  age_rating = relation( "CatalogEntry", uselist = False, primaryjoin = "Product.age_rating_id == CatalogEntry.id" )
  studio = relation( "CatalogEntry", uselist = False, primaryjoin = "Product.studio_id == CatalogEntry.id" )
  media = relation( "CatalogEntry", uselist = False, primaryjoin = "Product.media_id == CatalogEntry.id" )

  by_id   = classmethod( by_id )

  def __init__( self, name ):
    self.name  = name


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

ProductLanguage = Table( "product_language", metadata,
  Column( "product_id", Integer, ForeignKey( Product.id ) ),
  Column( "language_id", Integer, ForeignKey( CatalogEntry.id ) )
)

Product.languages = relation( CatalogEntry, secondary = ProductLanguage )

ProductSubtitle = Table( "product_subtitle", metadata,
  Column( "product_id", Integer, ForeignKey( Product.id ) ),
  Column( "subtitle_id", Integer, ForeignKey( CatalogEntry.id ) )
)

Product.subtitles = relation( CatalogEntry, secondary = ProductSubtitle )

