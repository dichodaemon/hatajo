# -*- coding: utf-8 -*-

import cherrypy
import logging
from public import Public
from admin import Admin
from services import Services


logger = logging.getLogger( "WebApp" )

#-------------------------------------------------------------------------------

class WebApp( object ):
  def __init__( self, backend ):
    self.backend = backend
    self.public  = Public( backend )
    self.admin   = Admin( backend )
    self.services = Services( backend )
    
  #-----------------------------------------------------------------------------

  @cherrypy.expose
  def index( self ):
    raise cherrypy.HTTPRedirect( "/public/" )

