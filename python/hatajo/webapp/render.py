# -*- coding: utf-8 -*-

import sys
import os
from mako import exceptions

BASE_DIR = os.path.abspath( os.path.join( os.path.dirname( __file__ ), "..", "..", ".." ) )
 
import cherrypy
from   cherrypy import Tool, tools
import gettext
import tidy
from   mako.template import Template
from   mako.lookup   import TemplateLookup

lookup = TemplateLookup( 
  directories = [os.path.join( BASE_DIR, 'templates' )],
  format_exceptions = True,
  output_encoding = "utf-8"
)

#-------------------------------------------------------------------------------

def transform( template = None ):
  oldHandler = cherrypy.request.handler
  def wrapper( *args, **kargs ):
    params = oldHandler( *args, **kargs ) 
    
    if template and type( params ) != list:
      params["_js"] = []
      params["_css"] = []
      params["_code"] = []
      params["_head"] = []
      params["user"] = cherrypy.session.get( "user" )
      t = lookup.get_template( template )
      t.output_encoding = 'utf-8'
      result = t.render_unicode( **params )
      if template[-5:] == ".html":
        return str( tidy.parseString( 
          result, 
          output_xhtml = True, 
          indent = True, 
          tidy_mark = 0, 
          output_encoding = "utf8",
          wrap = 120
        ) )
      else:
        return result


  cherrypy.request.handler = wrapper

#-------------------------------------------------------------------------------

tools.render = Tool( "before_handler", transform )
