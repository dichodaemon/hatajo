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

  #-----------------------------------------------------------------------------

  def login( self, user_name, password ):
    user = self.backend.authenticate( user_name, password )
    if type( user ) == dict:
      cherrypy.session["user"] = user
      return True
    return False

  #-----------------------------------------------------------------------------

  def logout( self ):
    cherrypy.session["user"]      = None

  #-----------------------------------------------------------------------------

  def callable( self, **kargs ):
    for k, v in kargs.items():
      if hasattr( self, k ):
        if not getattr( self, k )( v ):
          if self.logged():
            raise cherrypy.HTTPRedirect( "/public/forbidden" )
          else:
            destination  = urllib.quote( cherrypy.request.request_line.split()[1] )
            raise cherrypy.HTTPRedirect( "/public/login?destination=%s" % destination )

  #-----------------------------------------------------------------------------

  def member_of( self, groups ):
    user = cherrypy.session.get( "user" )
    if user and "groups" in user:
      for g in groups:
        if g in user["groups"]["values"]:
          return True
      return False
    return False

  #-----------------------------------------------------------------------------

  def name_is( self, userNames ):
    user = cherrypy.session.get( "user" )
    if user:
      return user["name"] in userNames
    return False

  #-----------------------------------------------------------------------------

  def logged( self, value = True ):
    return cherrypy.session.has_key( "user" ) and cherrypy.session["user"] != None

cherrypy.tools.form_authentication = FormAuthentication()
