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
  def search_results( self, filter="", sort_by="name", descending=True, page=0, limit=10 ):
    result = {
      "pageTitle": u"Su búsqueda",
      "base_url": "/public/search_results?",
      "sort_fields": [("name", u"Nombre"), ("year", u"Año")],
    }
    result.update( 
      helpers.pager_helper( 
        self.backend.pager, "Product", "name", filter, sort_by, descending, page, limit 
      )
    )
    pprint.pprint( result, width = 80 )
    return result

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "public/film_info.html" )
  def film_info( self, id ):
    result = {
      "pageTitle": u"Detalles de la película",
      "data": self.backend.product_info( id ),
      "product_reviews": self.backend.reviews( id )
    }
    return result

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "public/product_reviews.html" )
  def product_reviews( self, id, filter="", sort_by="name", descending=True, page=0, limit=5, rating = 0 ):
    result = {
      "pageTitle": u"Comentarios de los usuarios",
      "data": self.backend.product_info( id ),
      "base_url": "/public/product_reviews?id=%s&" % id,
      "sort_fields": [("name", u"Nombre"), ("date", u"Fecha"), ("rating", "Nota")],
      "rating": rating
    }
    if rating != None and rating != "" and rating != "0" and rating != 0:
      select = [( "product_id", id ), ( "rating", int( rating ) )]
    else:
      select = [( "product_id", id )]

    result.update( 
      helpers.pager_helper( 
        self.backend.pager, "Review", "name", filter, sort_by, descending, page,
        limit, select
      )
    )
    pprint.pprint( result, width = 80 )
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

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "public/review_edit.html" )
  def review_edit( self, **kargs  ):
    pprint.pprint( kargs, width = 80 )
    kargs = helpers.cleanup_arguments( kargs )
    if "rating" in kargs:
      if kargs["rating"].strip() != "":
        kargs["rating"] = float( kargs["rating"] )
      else:
        kargs["rating"] = 0
    kargs, warnings, errors = self.backend.review_update( kargs )
    if kargs["id"] != "new" and len( errors ) == 0:
      raise cherrypy.HTTPRedirect( "/public/film_info?id=%i" % kargs["product_id"] )
    result = {
      "pageTitle": u"Escriba su comentario",
      "product": self.backend.product_info( kargs["product_id"] ),
      "errors": [],
      "warnings": [],
      "data": kargs
    }
    return result
