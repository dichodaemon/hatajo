# -*- coding: utf-8 -*-

import db
from db import session, CatalogEntry
import hashlib
import pprint
import datetime
import random
import math
from collections import defaultdict

import helpers

class Backend( object ):
  def __init__( self, key ):
    self.key = key


  def authenticate( self, email, password ):
    user = db.User.by_email( email )
    if user == None:
      return False
    else:
      if user.authenticate( password, self.key ):
        return helpers.get( db.User ).to_dictionary( user )
      else:
        return True

  def new_user( self, user, email, email_confirm, password, password_confirm ):
    u = db.User.by_email( email )
    if u != None:
      return {}, {}, { "email": [u"La dirección '%s' ya está dada de alta, escoja otra." % email] }
    errors = defaultdict( list )
    if len( user.strip() ) < 4:
      errors["user"].append( "El nombre de usuario debe tener al menos 4 caracteres." )
    if email != email_confirm:
      errors["email_confirm"].append( "La dirección de correo y la confirmación no coinciden" )
    if len( password.strip() ) < 6:
      errors["password"].append( "La contraseña debe tener 6 caracteres o más" )
    if password != password_confirm:
      errors["password_confirm"].append( "La contraseña y la confirmación deben coincidir" )
    if len( errors ) == 0:
      u = db.User()
      u.email = email
      u.set_password( password, self.key )
      u.name = user
      u.groups.append( db.session().query( db.CatalogEntry )\
                       .filter( db.CatalogEntry.catalog_name == "user_groups" )\
                       .filter( db.CatalogEntry.value == "Usuarios" )\
                       .first() )
      db.session().add( u )
      db.session().commit()
      return helpers.get( db.User ).to_dictionary( u ), {}, {}
    return {}, {}, dict( errors )

  def find_in_catalog( self, catalog_name, term ):
    result = db.session().query( db.CatalogEntry )\
      .filter( db.CatalogEntry.catalog_name == catalog_name )\
      .filter( db.CatalogEntry.value.like( "%%%s%%" % term ) )\
      .all()
    return [
      { "id": v.id, "value": v.value } for v in result
    ]

  def catalog( self, catalog_name ):
    result = db.session().query( db.CatalogEntry )\
      .filter( db.CatalogEntry.catalog_name == catalog_name )\
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
      if "images" in arguments:
        if len( arguments["images"]["ids"] ) == 0:
          errors["images"].append( u"Es necesario dar de alta una imagen" )
        if len( filter( lambda x: x, arguments["images"]["values"] ) ) == 0:
          errors["images"].append( u"Es necesario dar de alta una imagen principal" )
      else:
        errors["images"].append( u"Es necesario dar de alta una imagen" )
      if len( errors ) == 0:
        helpers.get( db.Product ).to_record( arguments, product )
        db.session().add( product )
        db.session().commit()
        arguments = helpers.get( db.Product ).to_dictionary( product )
    else:
      arguments = helpers.get( db.Product ).to_dictionary( product )
    print
    pprint.pprint( arguments, width = 80 )
    return arguments

  def product_info( self, id ):
    product = db.Product.by_id( id )
    result = helpers.get( db.Product ).to_dictionary( product )
    return result

  def products( self ):
    data = db.session().query( db.Product ).all()
    result = []
    for p in data:
      d = helpers.get( db.Product ).to_dictionary( p )
      result.append( d )
    return result

  def product_pager( self, table, filter_field, filter, sort_by, descending, page, limit, prefilter=[] ):
    table = db.__dict__[table]
    def build_query( query ):
      for field, value in prefilter:
        query = query.filter( getattr( table, field ) == value )
      if filter != "":
        for f in filter.split():
          query = query.filter( getattr( table, filter_field ).like( "%%%s%%" % filter ) )
      if not descending:
        query = query.order_by( db.func.lower( getattr( table, sort_by ) ).asc() )
      else:
        query = query.order_by( db.func.lower( getattr( table, sort_by ) ).desc() )
      query = query.distinct()
      return query

    result = build_query( db.session().query( table ) )
    count  = build_query( db.session().query( db.func.count( db.distinct( table.id ) ) ) ).one()[0]
    result = result.limit( limit ).offset( page * limit ).all()

    result = [ 
        helpers.get( table ).to_dictionary( p )
      for p in result
    ]
    print count, limit
    return result, int( math.ceil( 1.0 * count / limit ) )

  def pager( self, table, filter_field, filter, sort_by, descending, page, limit, prefilter=[] ):
    table = db.__dict__[table]
    def build_query( query ):
      for field, value in prefilter:
        query = query.filter( getattr( table, field ) == value )
      if filter != "":
        for f in filter.split():
          query = query.filter( getattr( table, filter_field ).like( "%%%s%%" % filter ) )
      if not descending:
        query = query.order_by( db.func.lower( getattr( table, sort_by ) ).asc() )
      else:
        query = query.order_by( db.func.lower( getattr( table, sort_by ) ).desc() )
      query = query.distinct()
      return query

    result = build_query( db.session().query( table ) )
    count  = build_query( db.session().query( db.func.count( db.distinct( table.id ) ) ) ).one()[0]
    result = result.limit( limit ).offset( page * limit ).all()

    result = [ 
        helpers.get( table ).to_dictionary( p )
      for p in result
    ]
    print count, limit
    return result, int( math.ceil( 1.0 * count / limit ) )

  @helpers.main_form
  def inventory_update( self, arguments, warnings, errors ):
    print "-" * 80
    pprint.pprint( arguments, width = 80 )

    inventory = db.Inventory()
    if "product_id" in arguments:
      inventory.product = db.Product.by_id( arguments["product_id"] )
    inventory.date = datetime.datetime.now()

    if len( arguments ) > 2:
      if arguments["product_id"].strip() == "":
        errors["normal_price"].append( u"No se seleccionó un producto" )
      if int( arguments["normal_price"].strip() ) <= 0:
        errors["normal_price"].append( u"Es necesario entrar un valor positivo para el precio" )
      if int( arguments["discounted_price"].strip() ) <= 0:
        errors["discounted_price"].append( u"Es necesario entrar un valor positivo para el precio" )
      if int( arguments["units"].strip() ) <= 0:
        errors["units"].append( u"Es necesario entrar un valor positivo para las unidades" )
      if len( errors ) == 0:
        helpers.get( db.Inventory ).to_record( arguments, inventory )
        db.session().add( inventory )
        db.session().commit()
        arguments = helpers.get( db.Inventory ).to_dictionary( inventory )
    else:
      arguments = helpers.get( db.Inventory ).to_dictionary( inventory )
    arguments["product"] = helpers.get( db.Product ).to_dictionary( inventory.product )
    print
    pprint.pprint( arguments, width = 80 )
    return arguments

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
    return {
      "name": result.name,
      "hash": result.hash,
      "content": result.content.encode( "base64" ),
      "content_type": result.content_type
    }

  def product_delete( self, id ):
    product = db.Product.by_id( id )
    if id == None:
      return False
    db.session().delete( product )
    db.session().commit()
    return True

  @helpers.main_form
  def ad_update( self, arguments, warnings, errors ):
    print "-" * 80
    pprint.pprint( arguments, width = 80 )

    if arguments["id"] == "new": 
      ad = db.Ad()
    else:
      ad = db.Ad.by_id( arguments["id"] )

    if len( arguments ) > 1:
      if arguments["name"].strip() == "":
        errors["name"].append( u"Es necesario asignar un nombre al anuncio" )
      if len( errors ) == 0:
        helpers.get( db.Ad ).to_record( arguments, ad )
        db.session().add( ad )
        db.session().commit()
        arguments = helpers.get( db.Ad ).to_dictionary( ad )
    else:
      arguments = helpers.get( db.Ad ).to_dictionary( ad )
    pprint.pprint( arguments, width = 80 )
    return arguments

  def ad_delete( self, id ):
    record = db.Ad.by_id( id )
    if id == None:
      return False
    db.session().delete( record )
    db.session().commit()
    return True

  def ad( self, ad_type ):
    ad_type = db.session().query( db.CatalogEntry )\
              .filter( db.CatalogEntry.catalog_name == "ad_types" )\
              .filter( db.CatalogEntry.value == ad_type )\
              .first()
    result = db.session().query( db.Ad )\
             .filter( db.Ad.ad_type == ad_type )\
             .filter( db.Ad.valid_until > datetime.datetime.now().date() )\
             .filter( db.Ad.enabled == True )\
             .all()
    result = random.sample( result, 1 )[0]
    return helpers.get( db.Ad ).to_dictionary( result )

  @helpers.main_form
  def review_update( self, arguments, warnings, errors ):
    print "-" * 80
    pprint.pprint( arguments, width = 80 )

    if arguments["id"] == "new": 
      record = db.Review()
    else:
      record = db.Review.by_id( arguments["id"] )

    if len( arguments ) > 1:
      if arguments["name"].strip() == "":
        errors["name"].append( u"Es necesario asignar un nombre al comentario" )
      if arguments["alias"].strip() == "":
        errors["alias"].append( u"Es necesario capturar un nombre de usuario" )
      if len( arguments["content"].split() ) < 10:
        errors["content"].append( u"El comentario debe tener al menos 10 palabras" )
      if len( errors ) == 0:
        helpers.get( db.Review ).to_record( arguments, record )
        record.date = datetime.datetime.now()
        db.session().add( record )
        db.session().commit()
        arguments = helpers.get( db.Review ).to_dictionary( record )
    else:
      arguments = helpers.get( db.Review ).to_dictionary( record )
    pprint.pprint( arguments, width = 80 )
    return arguments

  def reviews( self, product_id ):
    record = db.Product.by_id( product_id )
    result =  [
      helpers.get( db.Review ).to_dictionary( r )
      for r in record.reviews
    ]
    pprint.pprint( result, width = 80 )
    return result

  @helpers.main_form
  def user_update( self, arguments, warnings, errors ):
    print "-" * 80
    pprint.pprint( arguments, width = 80 )

    if arguments["id"] == "new": 
      user = db.User()
    else:
      user = db.User.by_id( arguments["id"] )

    if len( arguments ) > 1:
      if arguments["name"].strip() == "":
        errors["name"].append( u"Es necesario asignar un nombre al usuario" )
      if arguments["email"].strip() == "":
        errors["name"].append( u"Es necesario asignar un email al usuario" )
      if len( errors ) == 0:
        helpers.get( db.User ).to_record( arguments, user )
        db.session().add( user )
        db.session().commit()
        arguments = helpers.get( db.User ).to_dictionary( user )
    else:
      arguments = helpers.get( db.User ).to_dictionary( user )
    print
    pprint.pprint( arguments, width = 80 )
    return arguments
