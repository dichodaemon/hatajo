# -*- coding: utf-8 -*-

import render
import cherrypy
import os
import json
import logging
import re
import time
import datetime

BASE_DIR = os.path.abspath( os.path.join( os.path.dirname( __file__ ), "..", "..", ".." ) )

logger = logging.getLogger( "WebApp" )

#-------------------------------------------------------------------------------

class WebApp( object ):
  def __init__( self, backend ):
    self.backend = backend
    
  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "index.html" )
  def index( self ):
    result = {
      "pageTitle": u"Página principal"
    }
    return result

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "search_results.html" )
  def search_results( self ):
    result = {
      "pageTitle": u"Su búsqueda"
    }
    return result

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "film_info.html" )
  def film_info( self ):
    result = {
      "pageTitle": u"Detalles de la película"
    }
    return result

