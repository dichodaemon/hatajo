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
  @cherrypy.tools.render( template = "public/forbidden.html" )
  def forbidden( self ):
    result = {
      "pageTitle": u"Página inexistente o restringida"
    }
    return result

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "public/login.html" )
  def login( self, email=None, existing=True, password=None, destination="" ):
    if existing == "False":
      raise cherrypy.HTTPRedirect( "/public/new_user?email=%s&destination=%s" % ( email, destination ) )
    if email and password:
      if cherrypy.tools.form_authentication.login( email, password ):
        if destination != "":
          raise cherrypy.HTTPRedirect( destination )
        else:
          raise cherrypy.HTTPRedirect( "/" )
    result = {
      "pageTitle": u"Página principal",
      "destination": destination
    }
    return result

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "public/new_user.html" )
  def new_user( self, user="", email="", email_confirm="", password="", password_confirm="", destination="" ):
    errors = {}
    if email_confirm != "":
      kargs, warnings, errors = self.backend.new_user( user, email, email_confirm, password, password_confirm )
      if len( errors ) == 0:
        raise cherrypy.HTTPRedirect( "/public/login?email=%s" % email )
    data = { 
      "user": user,
      "email": email, 
      "email_confirm": email_confirm, 
      "password": password, 
      "password_confirm": password_confirm 
    }
    result = {
      "pageTitle": u"Alta de cuenta",
      "data": data,
      "destination": destination,
      "errors": errors,
      "warnings": {}
    }
    return result

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  def logout( self ):
    cherrypy.tools.form_authentication.logout()
    raise cherrypy.HTTPRedirect( "/" )

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "public/search_results.html" )
  def search_results( self, filter="", genre="", sort_by="name", descending=True, page=0, limit=10 ):
    if genre == "":
      genre_name = "Resultados"
    else:
      genre_name = self.backend.find_id_in_catalog( int( genre ) )["value"]
    result = {
      "pageTitle": u"Su búsqueda",
      "base_url": "/public/search_results?",
      "genre_name": genre_name,
      "sort_fields": [("name", u"Nombre"), ("year", u"Año")],
    }
    result.update( 
      helpers.product_helper( 
        self.backend.product_pager, "name", filter, sort_by, descending, page, limit, genre 
      )
    )
    pprint.pprint( result, width = 80 )
    return result

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "public/film_info.html" )
  def film_info( self, id ):
    visited = cherrypy.session.get( "visited", [] )
    visited = visited[:10]
    visited.insert( 0, int( id ) )
    cherrypy.session["visited"] = visited

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
        self.backend.pager, "Review", "name", filter, sort_by, descending, int( page ) * int( limit ),
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
  def recommendation( self, title, method = "", layout="horizontal" ):
    done = False
    while not done:
      try:
        done = True
        if method == "random":
          elements = filter( lambda r: r["normal_price"] > 0, self.backend.products() )
          random.shuffle( elements )
        elif method == "recent":
          added = set()
          elements = []
          for id in cherrypy.session.get( "visited", [] ):
            if not id in added:
              elements.append( self.backend.product_info( id ) )
              added.add( id )
          for p in self.backend.products():
            if not p["id"] in added:
              elements.append( p )
              added.add( p["id"] )
      except httplib.CannotSendRequest:
        time.sleep( random.random() )
        done = False
      except httplib.ResponseNotReady:
        time.sleep( random.random() )
        done = False
    return {
      "data": {
        "layout": layout,
        "title": title,
        "elements": elements
      },
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

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "public/add_to_cart.html" )
  def add_to_cart( self, id, quantity  ):
    data = self.backend.product_info( id )
    quantity = int( quantity )
    if not cherrypy.session.has_key( "cart" ) or cherrypy.session["cart"] == None:
      cherrypy.session["cart"] = { "items": [], "total": 0, "item_count": 0 }
    found = False
    old_quantity = 0
    for item in cherrypy.session["cart"]["items"]:
      if item["id"] == id:
        item["quantity"] += quantity
        old_quantity = quantity
        found = True
    if not found:
      cherrypy.session["cart"]["items"].append( { "id": id, "quantity": quantity, "name": data["name"], "price": data["discounted_price"] } )
    cherrypy.session["cart"]["total"] += data["discounted_price"] * quantity
    cherrypy.session["cart"]["item_count"] += quantity
    result = {
      "pageTitle": u"Agregar al carrito de compras",
      "data": data,
      "quantity": quantity + old_quantity,
      "cart": cherrypy.session["cart"]
    }
    return result

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "public/cart.html" )
  def cart( self ):
    if not cherrypy.session.has_key( "cart" ):
      cherrypy.session["cart"] = { "items": [], "total": 0, "item_count": 0 }
    cart = cherrypy.session["cart"]
    for i in cart["items"]:
      i["data"] = self.backend.product_info( i["id"] )
      
    result = {
      "pageTitle": u"Editar carrito de compras",
      "cart": cherrypy.session["cart"]
    }
    return result
    
  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "public/order_processed.html" )
  def order_processed( self ):
    result = {
      "pageTitle": u"Gracias por su pedido",
      "fields": cherrypy.session["fields"]
    }
    return result
