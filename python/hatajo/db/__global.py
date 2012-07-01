# -*- coding: utf-8 -*-

from sqlalchemy                 import Table, Column, Integer, Date, DateTime
from sqlalchemy                 import String, MetaData, ForeignKey
from sqlalchemy                 import LargeBinary
from sqlalchemy                 import Boolean, Float
from sqlalchemy                 import or_, and_, not_, case
from sqlalchemy                 import func, distinct
from sqlalchemy.orm             import relation
from sqlalchemy.orm             import mapper, backref

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import __builtin__

#-------------------------------------------------------------------------------

Base = declarative_base()
metadata = Base.metadata

#-------------------------------------------------------------------------------

def init( uri, **kargs ):
  bid = __builtin__.__dict__
  if not bid.has_key( "engine" ):
    bid["engine"] = create_engine( 
      uri,
      **kargs
    )
  if not bid.has_key( "Session" ):
    bid["Session"] = scoped_session( sessionmaker( bind = engine ) )

def create( uri, **kargs ):
  global engine
  init( uri, **kargs )
  metadata.create_all( engine )

def session():
  return Session()

def all( cls ):
  return session().query( cls ).all()

def by_name( cls, name ):
  return session().query( cls ).filter( cls.name == name ).first()

def by_id( cls, id ):
  return session().query( cls ).filter( cls.id == id ).first()
