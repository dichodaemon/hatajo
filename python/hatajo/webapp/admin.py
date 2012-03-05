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
import helpers
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
  def product_list_elements( self, **args ):
    result = helpers.datatable_helper( self.backend, "Product", "name", ["name", "year" ], **args )
    result["aaData"] = [
      [
        "<a id='%s' href=/admin/product_edit?id=%s>%s</a>" % ( d["id"], d["id"],  d["name"] ),
        d["year"],
        ", ".join( [director for director in d["directors"]["values"]] )
      ]
      for d in result["aaData"]
    ]
    return json.dumps( result )

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "admin/product_edit.html" )
  def product_edit( self, **kargs ):
    kargs = helpers.cleanup_arguments( kargs )
    kargs, warnings, errors = self.backend.product_update( kargs )
    result = {
      "pageTitle": u"Información de producto",
      "errors": errors,
      "warnings": warnings,
      "data": kargs,
      "catalogs": {
        "norms": self.backend.catalog( "norms" )
      }
    }
    result.update( kargs )
    return result

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "admin/ad_list.html" )
  def ad_list( self ):
    result = {
      "pageTitle": u"Lista de anuncios"
    }
    return result


  #-----------------------------------------------------------------------------

  @cherrypy.expose
  def ad_list_elements( self, **args ):
    result = helpers.datatable_helper( self.backend, "Ad", "name", ["name", "enabled", "ad_type", "valid_until" ], **args )
    result["aaData"] = [
      [
        "<a id='%s' href=/admin/ad_edit?id=%s>%s</a>" % ( d["id"], d["id"],  d["name"] ),
        d["enabled"] and "si" or "no",
        d["ad_type"]["value"],
        d["valid_until"]
      ]
      for d in result["aaData"]
    ]
    return json.dumps( result )

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "admin/ad_edit.html" )
  def ad_edit( self, **kargs ):
    kargs = helpers.cleanup_arguments( kargs )
    kargs, warnings, errors = self.backend.ad_update( kargs )
    result = {
      "pageTitle": u"Edición de anuncio",
      "errors": errors,
      "warnings": warnings,
      "data": kargs,
      "catalogs": {
        "ad_types": self.backend.catalog( "ad_types" )
      }
    }
    result.update( kargs )
    return result
