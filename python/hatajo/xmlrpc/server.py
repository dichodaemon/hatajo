# -*- coding: utf-8 -*-

from twisted.web import xmlrpc
import logging

logger = logging.getLogger( "Server" )

#-------------------------------------------------------------------------------

class Server( xmlrpc.XMLRPC ):
  def __init__( self, obj ):
    xmlrpc.XMLRPC.__init__( self )
    self.object = obj
    logger.debug( self.object.__class__ )

  #-----------------------------------------------------------------------------

  def __getattr__( self, destination ):
    if hasattr( self.object, destination[7:] ):
      return getattr( self.object, destination[7:] )
    else:
      logger.error( "Method (%s) does not exist" % destination )
      logger.error( type( self.object ) )
      logger.error( self.object.__dict__.keys() )
      logger.error( self.__dict__.keys() )
      return False
