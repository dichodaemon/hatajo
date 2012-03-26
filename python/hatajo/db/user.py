# -*- coding: utf-8 -*-

from __global import *
from catalog_entry import CatalogEntry
import hmac
import hashlib

def by_email( cls, value ):
  return session().query( cls ).filter( cls.email == value ).first()

class User( Base ):
  __tablename__ = "users"
  id          = Column( Integer, primary_key = True )
  name        = Column( String )
  password    = Column( String )
  email       = Column( String, index = True )
  last_login  = Column( Date )

  by_email = classmethod( by_email )
  by_id    = classmethod( by_id )

  def set_password( self, password, key ):
    self.password = hmac.new( key, "%s:%s" % ( self.email, password ) ).hexdigest()

  def authenticate( self, password, key ):
    return self.password == hmac.new( key, "%s:%s" % ( self.email, password ) ).hexdigest()

UserGroup = Table( "user_groups", metadata,
  Column( "user_id", Integer, ForeignKey( User.id ) ),
  Column( "group_id", Integer, ForeignKey( CatalogEntry.id ) )
)

User.groups = relation( CatalogEntry, secondary = UserGroup )
