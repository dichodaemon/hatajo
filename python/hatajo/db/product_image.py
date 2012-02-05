# -*- coding: utf-8 -*-

from __global import *

def by_product_image( cls, product_id, image_id ):
  return session()\
          .query( cls )\
          .filter( cls.product_id == product_id )\
          .filter( cls.image_id == image_id )\
          .first()

class ProductImage( Base ):
  __tablename__ = 'product_images'
  id           = Column( Integer, primary_key = True )
  product_id   = Column( Integer, ForeignKey( "products.id" ) )
  image_id     = Column( Integer, ForeignKey( "binary_content.id" ) )
  main         = Column( Boolean )

  product = relation( 
    "Product", 
    backref = backref( "images", cascade="all,delete-orphan" ),
    uselist = False
  )

  image = relation( 
    "BinaryContent",
    uselist = False
  )

  by_id   = classmethod( by_id )
  by_product_image = classmethod( by_product_image )

  def __init__( self, product, image, main ):
    self.product = product
    self.image   = image
    self.main    = main

