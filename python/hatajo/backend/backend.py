# -*- coding: utf-8 -*-

import db
from db import session, CatalogEntry
import hashlib
import pprint

import helpers

class Backend( object ):
  def __init__( self ):
    pass

  def find_in_catalog( self, catalog_name, term ):
    result = db.session().query( db.CatalogEntry )\
      .filter( db.CatalogEntry.catalog_name == catalog_name )\
      .filter( db.CatalogEntry.value.like( "%%%s%%" % term ) )\
      .all()
    return [
      { "id": v.id, "value": v.value } for v in result
    ]

  @helpers.main_form
  def product_update( self, arguments, warnings, errors ):
    print "-" * 80
    pprint.pprint( arguments, width = 80 )

    if arguments["id"] == "new": 
      product = db.Product( arguments["name"] )
    else:
      product = db.Product.by_id( arguments["id"] )

    if len( arguments ) > 1:
      if arguments["name"].strip() == "":
        errors["name"].append( u"Es necesario asignar un nombre al producto" )
      if len( arguments["images"]["ids"] ) == 0:
        errors["images"].append( u"Es necesario dar de alta una imagen" )
      if len( filter( lambda x: x, arguments["images"]["values"] ) ) == 0:
        errors["images"].append( u"Es necesario dar de alta una imagen principal" )
      if len( errors ) == 0:
        helpers.product.to_record( arguments, product )
        db.session().add( product )
        db.session().commit()
        arguments = helpers.product.to_dictionary( product )
    else:
      arguments = helpers.product.to_dictionary( product )
    print
    pprint.pprint( arguments, width = 80 )
    return arguments

  def product_info( self, id ):
    print "-" * 80
    product = db.Product.by_id( id )
    result = helpers.product.to_dictionary( product )
    pprint.pprint( result, width = 80 )
    return result

  def products( self ):
    print "-" * 80
    result = db.session().query( db.Product ).all()
    result = [ 
        helpers.product.to_dictionary( p )
      for p in result
    ]
    pprint.pprint( result, width = 80 )
    return result

  def save_binary( self, filename, content_type, content ):
    content = content.decode( "base64" )
    hash = hashlib.md5( content ).hexdigest()
    result = db.session().query( db.BinaryContent )\
        .filter( db.BinaryContent.content_type == content_type )\
        .filter( db.BinaryContent.hash == hash )\
        .first()
    if result == None:
      result = db.BinaryContent( filename, hash, content, content_type )
      db.session().add( result )
      db.session().commit()
    return result.id

  def load_binary( self, id ):
    result = db.BinaryContent.by_id( id )
    print id, result
    return {
      "name": result.name,
      "hash": result.hash,
      "content": result.content.encode( "base64" ),
      "content_type": result.content_type
    }

