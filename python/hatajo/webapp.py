# -*- coding: utf-8 -*-

import render
import cherrypy
import os
import json
import logging
import re
import time
import datetime
from collections import defaultdict

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

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  @cherrypy.tools.render( template = "product_list.html" )
  def product_list( self ):
    result = {
      "pageTitle": u"Lista de prooductos"
    }
    return result

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  #@cherrypy.tools.render( template = "product_list.html" )
  def product_support( self, **args ):
    print args
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
  @cherrypy.tools.render( template = "product_edit.html" )
  def product_edit( self, **kargs ):
    kargs = self.backend.product_update( kargs )
    result = {
      "pageTitle": u"Información de producto"
    }
    result.update( kargs )
    return result

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  def find_in_catalog( self, catalog_name, term ):
    return json.dumps( self.backend.find_in_catalog( catalog_name, term ) )

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  def upload_image( self, qqfile ):
    content_type = "unknown"
    if qqfile[-4:] == ".png":
      content_type = "image/png"
    length = int( cherrypy.request.headers["Content-Length"] )
    content = cherrypy.request.body.read( length )
    result = self.backend.save_binary( qqfile, content_type, content.encode( "base64" ) )
    return json.dumps( result )

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  def ck_upload_image( self, CKEditor, CKEditorFuncNum, langCode, upload ):
    content = upload.file.read()
    content = content.encode( "base64" )
    filename = str( upload.filename )
    content_type = str( upload.content_type )
    result = self.backend.save_binary( filename, content_type, content )
    return """
    <html><body><script type="text/javascript">
    window.parent.CKEDITOR.tools.callFunction(%s, '%s','%s');
    </script></body></html>""" % ( CKEditorFuncNum, "/load_image?id=%i" % result, "" )
    

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  def load_image( self, id ):
    result = self.backend.load_binary( id )
    cherrypy.response.headers["Content-Type"] = result["content_type"]
    return result["content"].decode( "base64" )
