import db
from db import session, CatalogEntry
import hashlib

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

  def product_update( self, arguments ):
    import pprint
    if not "id" in arguments:
      arguments["id"] = "new"
      return arguments
    elif arguments["id"] == "new":
      pprint.pprint( arguments, width = 80 )
    for id, value in arguments.items():
      if (  len( id ) > 6
        and ( id[-5:] == "__ids" or id[-8:] == "__values" ) 
        and type( value ) != list
      ):
        arguments[id] = [value]
    for id, value in arguments.items():
      if len( id ) > 6 and id[-5:] == "__ids":
        catalog = id[:-5]
        ids    = value
        values = arguments[catalog + "__values"]
        for i in xrange( len( ids ) ):
          if ids[i] == "new":
            print "Adding value '%s' to catalog '%s'" % ( values[i], catalog )
            entry = CatalogEntry( catalog, values[i] ) 
            session().add( entry )
            session().commit()
            ids[i] = entry.id
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

