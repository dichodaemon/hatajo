# -*- coding: utf-8 -*-

import cherrypy
import json
import logging
import time
import random
import httplib
import urllib
import urllib2

logger = logging.getLogger( "WebApp" )

ppuser = "dichod_1337712011_biz_api1.gmail.com"
pppwd  = "1337712043"
ppsignature = "AvHZ32NRViZxM6AlqwC6-eHkFYd5AGlk0L.D2Y2BUiwZhwP1DQ6YGGEq"

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
    </script></body></html>""" % ( CKEditorFuncNum, "/services/load_image?id=%i" % result, "" )
    

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

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  def product_delete( self, id ):
    return json.dumps( self.backend.product_delete( int( id ) ) )

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  def ad_delete( self, id ):
    return json.dumps( self.backend.ad_delete( int( id ) ) )

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  def modify_cart( self, id, quantity  ):
    data = self.backend.product_info( id )
    quantity = int( quantity )
    selected = None
    for item in cherrypy.session["cart"]["items"]:
      if item["id"] == id:
        selected = item
        cherrypy.session["cart"]["total"] -= data["discounted_price"] * item["quantity"]
        cherrypy.session["cart"]["item_count"] -= item["quantity"]
        item["quantity"] = quantity
        cherrypy.session["cart"]["total"] += data["discounted_price"] * quantity
        cherrypy.session["cart"]["item_count"] += quantity 
    if selected != None and quantity == 0:
      cherrypy.session["cart"]["items"].remove( selected )
    raise cherrypy.HTTPRedirect( "/public/cart" )

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  def paypal_checkout( self ):
    url = "https://api-3t.sandbox.paypal.com/nvp"
    params = {}
    params["USER"]       = ppuser
    params["PWD"]        = pppwd
    params["SIGNATURE"]  = ppsignature
    params["VERSION"]    = "88.0"
    params["PAYMENTREQUEST_0_PAYMENTACTION"] = "Sale"
    params["RETURNURL"] = "http://hatajo.dizanvasquez.info/services/paypal_returnurl"
    params["CANCELURL"] = "http://www.yahoo.com"
    params["EMAIL"]     = cherrypy.session["user"]["email"]
    params["METHOD"] = "SetExpressCheckout"

    cart = cherrypy.session["cart"]
    params["PAYMENTREQUEST_0_AMT"] = cart["total"]
    params["PAYMENTREQUEST_0_ITEMAMT"] = cart["total"]
    for i in xrange( cart["item_count"] ):
      params["L_PAYMENT_REQUEST_0_NAME_%i" % i] = cart["items"][i]["name"].encode( "utf-8" )
      params["L_PAYMENT_REQUEST_0_QTY_%i" % i] = cart["items"][i]["quantity"]
      params["L_PAYMENT_REQUEST_0_AMT_%i" % i] = cart["items"][i]["quantity"] * cart["items"][i]["price"]
      params["L_PAYMENT_REQUEST_0_ITEM_CATEGORY_%i" % i] = "Physical"
      
    params = urllib.urlencode( params )
    print ">" * 80
    print params
    print ">" * 80
    request = urllib2.Request( url, params )
    response = urllib2.urlopen( request )
    fields = {}
    for l in urllib.unquote_plus( response.read() ).split( "&" ):
      key, value = l.split( "=" )
      fields[key] = value
    print "=" * 80
    print fields
    print "=" * 80
    if fields["ACK"] == "Success":
      print "paypal_checkout SUCCESS"
      raise cherrypy.HTTPRedirect( "https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token=%s" % fields["TOKEN"] )
    else:
      print "paypal_checkout FAILED"
      cherrypy.session["fields"] = fields
      raise cherrypy.HTTPRedirect( "/public/order_processed" )

  #-----------------------------------------------------------------------------

  @cherrypy.expose
  def paypal_returnurl( self, token, PayerID ):
    url = "https://api-3t.sandbox.paypal.com/nvp"
    params = {}
    params["USER"]       = ppuser
    params["PWD"]        = pppwd
    params["SIGNATURE"]  = ppsignature
    params["VERSION"]    = "88.0"
    params["TOKEN"] = token
    params["METHOD"] = "GetExpressCheckoutDetails"
    params = urllib.urlencode( params )
    request = urllib2.Request( url, params )
    response = urllib2.urlopen( request )
    fields = {}
    for l in urllib.unquote_plus( response.read() ).split( "&" ):
      key, value = l.split( "=" )
      fields[key] = value
    print "=" * 80
    print fields
    print "=" * 80
    if fields["ACK"] == "Success":
      cherrypy.session["fields"] = fields
      params = {}
      params["USER"]       = ppuser
      params["PWD"]        = pppwd
      params["SIGNATURE"]  = ppsignature
      params["VERSION"]    = "88.0"
      params["PAYMENTREQUEST_0_PAYMENTACTION"] = "Sale"
      params["PAYERID"] = PayerID
      params["PAYMENTREQUEST_0_AMT"] = fields["AMT"]
      params["TOKEN"] = token
      params["METHOD"] = "DoExpressCheckoutPayment"
      params = urllib.urlencode( params )
      request = urllib2.Request( url, params )
      response = urllib2.urlopen( request )
      fields = {}
      for l in urllib.unquote_plus( response.read() ).split( "&" ):
        key, value = l.split( "=" )
        fields[key] = value
      if fields["ACK"] == "Success":
        cherrypy.session["cart"] = { "items": [], "total": 0, "item_count": 0 }
      print "*" * 80
      print fields
      print "*" * 80
      raise cherrypy.HTTPRedirect( "/public/order_processed" )
      
