# -*- coding: utf-8 -*-

import cherrypy
import logging
import time
import pprint
import random
import httplib
import helpers

import render

logger = logging.getLogger( "WebApp" )

#-------------------------------------------------------------------------------

class Private( object ):
  def __init__( self, backend ):
    self.backend = backend
    
  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "private/index.html" )
  def index( self ):
    result = {
      "pageTitle": u"Página principal",
      "pageDescription": u"Mi cuenta"
    }
    return result

