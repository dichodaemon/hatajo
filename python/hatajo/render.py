# -*- coding: utf-8 -*-

import sys
import os
from mako import exceptions

BASE_DIR = os.path.abspath( os.path.join( os.path.dirname( __file__ ), "..", ".." ) )
  
import cherrypy
from   cherrypy import Tool, tools
import gettext
from   mako.template import Template
from   mako.lookup   import TemplateLookup

lookup = TemplateLookup( 
  directories = [os.path.join( BASE_DIR, 'templates' )],
  format_exceptions = True 
)

#-------------------------------------------------------------------------------

def transform( template = None ):
  oldHandler = cherrypy.request.handler
  def wrapper( *args, **kargs ):
    params = oldHandler( *args, **kargs ) 
    
    if template and type( params ) != list:
      params["_js"] = set()
      params["_css"] = set()
      params["_code"] = []
      t = lookup.get_template( template )
      t.output_encoding = 'utf-8'
      return t.render_unicode( **params )


  cherrypy.request.handler = wrapper

#-------------------------------------------------------------------------------

tools.render = Tool( "before_handler", transform )
