# -*- coding: utf-8 -*-

import db
import collections
import datetime

def main_form( f ):
  def result( self, arguments ):
    warnings = collections.defaultdict( list )
    errors   = collections.defaultdict( list )
    if not "id" in arguments:
      arguments["id"] = "new"
    else:
      arguments = f( self, arguments, warnings, errors )
    return arguments, dict( warnings ), dict( errors )
  return result

def get_catalog_entry( table, id, value ):
  c = None
  if id == "new":
    c = db.session().query( db.CatalogEntry )\
          .filter( db.CatalogEntry.catalog_name == table )\
          .filter( db.func.lower( db.CatalogEntry.value ) == db.func.lower( value ) )\
          .first()
    if c == None:
      c = db.CatalogEntry( table, value )
  else:
    c = db.CatalogEntry.by_id( id )
  return c

def get_product_image( table, product, image_id, value ):
  result = None
  for i in product.images:
    if i.image_id == image_id:
      result = i
      break
  if result == None:
    image = db.BinaryContent.by_id( image_id )
    result = db.ProductImage( product, image, value )
  else:
    result.value = value
  return result

def field_to_date( field ):
  return datetime.datetime.strptime( field, "%d/%m/%Y" )

def date_to_field( date ):
  if date != None:
    return date.strftime( "%d/%m/%Y" )
  else:
    return ""

def catalog_to_dictionary( entry ):
  result = {}
  if entry == None:
    result = { "id": "", "value": "", "table": "" }
  else:
    result = { 
      "id": entry.id, 
      "value": entry.value, 
      "table": entry.catalog_name
    }
  return result

def multi_to_dictionary( entries ):
  result = {
    "ids": [],
    "values": []
  }
  if entries != None and len( entries ) > 0:
    for e in entries:
      if not "table" in result:
        result["table"] = e.catalog_name
      result["ids"].append( e.id )
      result["values"].append( e.value )
  return result

def images_to_dictionary( images ):
  result = {
    "ids": [],
    "values": []
  }
  if images != None and len( images ) > 0:
    for i in images:
      result["ids"].append( i.image_id )
      result["values"].append( i.main )
  return result

class Helper( object ):
  def __init__( self, fields ):
    self.fields = fields

  def to_record( self, dic, record ):
    result = {}
    for f, info in self.fields.items():
      if not f in dic:
        if info == None and type( getattr( record, f ) ) == bool:
          setattr( record, f, False )
      else:
        value = dic[f]
        if info == None:
          setattr( record, f, value )
        elif info == "date":
          entry = field_to_date( value )
          setattr( record, f, entry ) 
        elif info == "catalog":
          entry = get_catalog_entry( value["table"], value["id"], value["value"] )
          setattr( record, f, entry ) 
        elif info == "dropdown_catalog":
          entry = db.CatalogEntry.by_id( value["id"] )
          setattr( record, f, entry ) 
        elif info == "multi":
          ids = value["ids"]
          values = value["values"]
          entries = []
          for i in xrange( len( ids ) ):
            entry = get_catalog_entry( value["table"], ids[i], values[i] )
            if entry != None:
              entries.append( entry )
          setattr( record, f, entries )
        elif info == "images":
          ids = value["ids"]
          values = value["values"]
          images = []
          for i in xrange( len( ids ) ):
            image = get_product_image( f, record, ids[i], values[i] )
            if image != None:
              images.append( image )
          setattr( record, f, images )

  def to_dictionary( self, record ):
    result = {}
    for f, info in self.fields.items():
      value = getattr( record, f )
      if info == None or info == "id":
        result[f] = value
        if value == None:
          result[f] = ""
      if info == "catalog":
        result[f] = catalog_to_dictionary( value )
      elif info == "multi":
        result[f] = multi_to_dictionary( value )
      elif info == "images":
        result[f] = images_to_dictionary( value )
      elif info == "date":
        result[f] = date_to_field( value )
    return result

