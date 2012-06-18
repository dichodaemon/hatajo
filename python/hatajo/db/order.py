# -*- coding: utf-8 -*-

from __global import *
from product import *

class Order( Base ):
  PAYMENT_PAYPAL = 0
  PAYMENT_GOOGLE = 1

  ORDER_PENDING   = 0
  ORDER_DELIVERED = 1
  ORDER_CANCELLED = 2

  DELIVERY_MEXPOST = 0
  DELIVERY_PAQPOST = 1

  __tablename__ = 'orders'
  id           = Column( Integer, primary_key = True )
  status       = Column( Integer )
  date         = Column( DateTime )
  user_id      = Column( Integer, ForeignKey( "users.id" ) )
  payment_type = Column( Integer )
  delivery_method = Column( Integer )
  name         = Column( String )
  country      = Column( String )
  city         = Column( String )
  state        = Column( String )
  street       = Column( String )
  postal_code  = Column( String )
  delivery_cost = Column( Float )
  total_amount = Column( Float )
  payment_info = Column( String )

  by_id = classmethod( by_id )


  user = relation( 
    "User",
    backref = backref( "orders", single_parent = True, cascade = "all, delete-orphan" )
  )


  detail = relation( 
    "OrderDetail",
    backref = backref( "order", single_parent = True, cascade = "all, delete-orphan" )
  )

class OrderDetail( Base ):
  __tablename__ = "order_detail"
  order_id      = Column( Integer, ForeignKey( Order.id ), primary_key = True )
  product_id    = Column( Integer, ForeignKey( Product.id ), primary_key = True )
  quantity      = Column( Integer )
  cost          = Column( Float )

  product = relation( 
    "Product", 
    uselist = False
  )
