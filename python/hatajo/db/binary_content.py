# -*- coding: utf-8 -*-

from __global import *

class BinaryContent( Base ):
  __tablename__ = 'binary_content'
  id        = Column( Integer, primary_key = True )
  name      = Column( String )
  hash      = Column( String )
  content   = Column( LargeBinary )
  content_type = Column( String )

  by_id   = classmethod( by_id )

  def __init__( self, name, hash, content, content_type ):
    self.name  = name
    self.hash  = hash
    self.content  = content
    self.content_type = content_type


