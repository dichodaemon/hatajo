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
  def product_support( self, **args ):
    return json.dumps( {
      "sEcho": args["sEcho"],
      "iTotalRecords": 10,
      "iTotalDisplayRecords": 10,
      "aaData": [
        [ 1, "a", True],
        [ 2, "b", True],
        [ 3, "c", True],
        [ 4, "d", True],
        [ 5, "e", True],
        [ 6, "f", True],
        [ 7, "g", True],
        [ 8, "h", True],
        [ 9, "i", True],
        [10, "j", True],
        [11, "k", True],
        [12, "l", True],
        [13, "m", True],
        [14, "n", True],
        [15, "o", True],
        [16, "p", True],
        [17, "q", True],
        [18, "r", True],
        [19, "s", True],
        [20, "t", True]
      ]
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
