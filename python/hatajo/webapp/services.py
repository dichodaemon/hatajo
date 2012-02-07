# -*- coding: utf-8 -*-

import cherrypy
import json
import logging
import time
import random
import httplib

logger = logging.getLogger( "WebApp" )

#-------------------------------------------------------------------------------

class Services( object ):
  def __init__( self, backend ):
    self.backend = backend
    
  #-----------------------------------------------------------------------------

  @cherrypy.expose
  def find_in_catalog( self, catalog_name, term ):
    result = json.dumps( self.backend.find_in_catalog( catalog_name, term ) )
    print result
    return result

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  def upload_image( self, qqfile ):
    content_type = "unknown"
    if qqfile[-4:] == ".png":
      content_type = "image/png"
    elif qqfile[-4:] == ".jpg":
      content_type = "image/jpg"
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
    done = False
    while not done:
      try:
        done = True
        result = self.backend.load_binary( id )
      except httplib.CannotSendRequest:
        time.sleep( random.random() )
        done = False
      except httplib.ResponseNotReady:
        time.sleep( random.random() )
        done = False
    cherrypy.response.headers["Content-Type"] = result["content_type"]
    return result["content"].decode( "base64" )

