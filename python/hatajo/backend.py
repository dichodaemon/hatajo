import db

class Backend( object ):
  def __init__( self ):
    pass

  def find_in_catalog( self, catalog_name, term ):
    result = db.session().query( db.Catalogs )\
      .filter( db.Catalogs.catalog_name == catalog_name )\
      .filter( db.Catalogs.value.like( "%%%s%%" % term ) )\
      .all()
    return [
      { "id": v.id, "value": v.value } for v in result
    ]
