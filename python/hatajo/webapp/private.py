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

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "private/confirm_order.html" )
  def confirm_order( self ):
    if not cherrypy.session.has_key( "cart" ):
      cherrypy.session["cart"] = { "items": [], "total": 0, "item_count": 0 }
    cart = cherrypy.session["cart"]
    for i in cart["items"]:
      i["data"] = self.backend.product_info( i["id"] )    
    result = {
      "pageTitle": u"Confirme su Órden",
      "pageDescription": u"Confirmar órden",
      "cart": cart
    }
    return result
