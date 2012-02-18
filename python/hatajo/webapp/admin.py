# -*- coding: utf-8 -*-

import render
import cherrypy
import os
import json
import logging
import re
import time
import datetime
import pprint
from collections import defaultdict
from helpers import cleanup_arguments
import random
import httplib
import time

BASE_DIR = os.path.abspath( os.path.join( os.path.dirname( __file__ ), "..", "..", ".." ) )

logger = logging.getLogger( "WebApp" )

#-------------------------------------------------------------------------------

class Admin( object ):
  def __init__( self, backend ):
    self.backend = backend
    
  #-----------------------------------------------------------------------------

  @cherrypy.expose
  def index( self ):
    raise cherrypy.HTTPRedirect( "/admin/product_edit" )

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "admin/product_list.html" )
  def product_list( self ):
    result = {
      "pageTitle": u"Lista de productos"
    }
    return result

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  #@cherrypy.tools.render( template = "product_list.html" )
  def product_pager( self, **args ):
    pprint.pprint( args, width = 80 )
    data = self.backend.product_pager( 
      args["sSearch"],
      int( args["iDisplayLength"] ),
      int( args["iDisplayStart"] )
    )
    data = [
      [
        "<a href=/admin/product_edit?id=%s>%s</a>" % ( d["id"],  d["name"] ),
        ", ".join( d["actors"]["values"] )
      ]
      for d in data
    ]
    pprint.pprint( data, width = 80 )
    return json.dumps( {
      "sEcho": args["sEcho"],
      "iTotalRecords": 10,
      "iTotalDisplayRecords": 10,
      "aaData": data 
    } )

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "admin/product_edit.html" )
  def product_edit( self, **kargs ):
    kargs = cleanup_arguments( kargs )
    kargs, warnings, errors = self.backend.product_update( kargs )
    result = {
      "pageTitle": u"Información de producto",
      "errors": errors,
      "warnings": warnings,
      "data": kargs
    }
    result.update( kargs )
    return result
