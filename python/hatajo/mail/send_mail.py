# -*- coding: utf-8 -*-

import sys
import os

BASE_DIR = os.path.abspath( os.path.join( os.path.dirname( __file__ ), "..", "..", ".." ) )
 
from mako import exceptions
from mako.template import Template
from mako.lookup   import TemplateLookup

import smtplib
from email.mime.text import MIMEText

lookup = TemplateLookup( 
  directories = [os.path.join( BASE_DIR, 'templates' )],
  format_exceptions = True,
  output_encoding = "utf-8"
)

def send_mail( subject, sender, to, template, data ):
  t = lookup.get_template( template )
  t.output_encoding = 'utf-8'
  msg = MIMEText( t.render_unicode( data = data ).encode( "utf-8" ), "html", "utf-8" )

  msg["subject"] = subject
  msg["from"]    = sender
  msg["to"]      = ", ".join( to )
  s = smtplib.SMTP( "localhost" )
  s.sendmail( sender, to, msg.as_string() )


if __name__ == "__main__":
  data = {}
  data["recipient"] = u"Dizan"
  data["user"] = {"name": u"Coques"}
  data["date"] = u"12-10-2025"
  data["payment_type"] = 0
  data["name"] = u"Comprador"
  data["street"] = u"Gob. de Jalisco #8 Casa 1"
  data["postal_code"] = "62350"
  data["city"] = u"Cuernavaca"
  data["state"] = u"Morelos"
  data["country"] = u"Mexico"
  data["total_amount"] = 31415
  data["detail"] = [
    { 
      "product": { "name": u"La de la mochila azul" },
      "quantity": 10,
      "cost": 50
    }
  ]
  send_mail( 
    "Prueba", "gorgonzola@queso.com", ["dichodaemon@gmail.com"], 
    "mail/new_order.txt", data 
  )
