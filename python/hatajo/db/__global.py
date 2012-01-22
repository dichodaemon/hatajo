# -*- coding: utf-8 -*-

from sqlalchemy                 import Table, Column, Integer, Date, DateTime
from sqlalchemy                 import String, MetaData, ForeignKey
from sqlalchemy                 import Boolean
from sqlalchemy                 import or_, and_, not_
from sqlalchemy.orm             import relation
from sqlalchemy.orm             import mapper, backref

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

#-------------------------------------------------------------------------------

Base     = declarative_base()
metadata = Base.metadata

engine  = None
Session = None

#-------------------------------------------------------------------------------

def init( uri, **kargs ):
  global engine, Session
  engine   = create_engine( 
    uri,
    **kargs
  )
  Session = scoped_session( sessionmaker( bind = engine ) )

def create( uri, **kargs ):
  global engine
  init( uri, **kargs )
  metadata.create_all( engine )



def session():
  return Session()


def all( cls ):
  return session().query( cls ).all()

def byName( cls, name ):
  return session().query( cls ).filter( cls.name == name ).first()

def byId( cls, id ):
  return session().query( cls ).filter( cls.id == id ).first()
