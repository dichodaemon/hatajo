# -*- coding: utf-8 -*-

import cherrypy
import logging
import time
import pprint
import random
import httplib

import render

logger = logging.getLogger( "WebApp" )

#-------------------------------------------------------------------------------

class Public( object ):
  def __init__( self, backend ):
    self.backend = backend
    
  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "public/index.html" )
  def index( self ):
    result = {
      "pageTitle": u"Página principal"
    }
    return result

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "public/search_results.html" )
  def search_results( self ):
    result = {
      "pageTitle": u"Su búsqueda",
      "data": self.backend.products()
    }
    return result

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "public/film_info.html" )
  def film_info( self, id ):
    result = {
      "pageTitle": u"Detalles de la película",
      "data": self.backend.product_info( id )
    }
    return result

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "public/product_list.html" )
  def product_list( self ):
    result = {
      "pageTitle": u"Lista de productos"
    }
    return result

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "public/recommendation.html" )
  def recommendation( self, title, method = "" ):
    done = False
    while not done:
      try:
        done = True
        elements = self.backend.products()
        random.shuffle( elements )
      except httplib.CannotSendRequest:
        time.sleep( random.random() )
        done = False
      except httplib.ResponseNotReady:
        time.sleep( random.random() )
        done = False
    return {
      "data": {
        "title": title,
        "elements": elements
      }
    }

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  def ad( self, ad_type ):
    while True:
      try:
        return self.backend.ad( ad_type )["content"]
      except httplib.CannotSendRequest:
        time.sleep( random.random() )
      except httplib.ResponseNotReady:
        time.sleep( random.random() )
