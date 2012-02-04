# -*- coding: utf-8 -*-

import cherrypy
import urllib
import hashlib
import os

ADMINISTRATORS = 0
USERS          = 1
CLIENTS        = 2

#-------------------------------------------------------------------------------

class FormAuthentication( cherrypy.Tool ):
  
  #-----------------------------------------------------------------------------

  def __init__( self ):
    self._point      = "before_handler"
    self._name       = None
    self._priority   = 50
    self.backend     = None
    self.cookieName  = "b_blue"

  #-----------------------------------------------------------------------------

  def login( self, username, password ):
    user = self.backend.authenticate( username, password )
    if user:
      sessionId  = hashlib.md5( os.urandom( 32 ) ).hexdigest()
      cherrypy.session["sessionId"] = sessionId
      cherrypy.session["user"] = user
      try:
        cherrypy.response.cookie["%s_sid" % self.cookieName] = sessionId
      except KeyError:
        pass
      return True
    return False

  #-----------------------------------------------------------------------------

  def logout( self ):
    cherrypy.session["sessionId"] = None
    cherrypy.session["user"]      = None
    try:
      cherrypy.response.cookie["%s_sid" % self.cookieName] = ""
      cherrypy.response.cookie["%s_sid" % self.cookieName]["expires"] = 0
    except KeyError:
      pass

  #-----------------------------------------------------------------------------

  def callable( self, **kargs ):
    for k, v in kargs.items():
      if hasattr( self, k ):
        if not getattr( self, k )( v ):
          if self.logged():
            if cherrypy.request.path_info != "/":
              raise cherrypy.HTTPRedirect( "/" )
          else:
            #~ raise cherrypy.HTTPRedirect( "/login?destination=%s" % destination )
            raise cherrypy.HTTPRedirect( "/login" )

  #-----------------------------------------------------------------------------

  def member_of( self, groups ):
    user = cherrypy.session.get( "user" )
    if user and "group" in user:
      return user["group"] in groups
    return False

  #-----------------------------------------------------------------------------

  def name_is( self, userNames ):
    user = cherrypy.session.get( "user" )
    if user:
      return user["username"] in userNames
    return False

  #-----------------------------------------------------------------------------

  def logged( self, value = True ):
    result     = True
    try:
      sessionId  = cherrypy.request.cookie["%s_sid" % self.cookieName].value
    except KeyError:
      result = False
      
    if result:
      result = cherrypy.session.get( "sessionId" ) == sessionId
    if value:
      return result
    else:
      return not result


cherrypy.tools.form_authentication = FormAuthentication()
