# -*- coding: utf-8 -*-

import db
from helper import Helper, main_form
from product_helper import ProductHelper

helpers = {}
helpers[db.Product] = ProductHelper( {
  "id": "id",
  "name": None,
  "original_name": None,
  "year": None,
  "genres": "multi",
  "actors": "multi",
  "directors": "multi",
  "norm": "catalog",
  "screen_format": "catalog",
  "format": "catalog",
  "medias": "multi",
  "languages": "multi",
  "subtitles": "multi",
  "regions": "multi",
  "item_count": None,
  "age_rating": "catalog",
  "productor": "catalog",
  "distributor": "catalog",
  "duration": None,
  "rtc": None,
  "bar_code": None,
  "images": "images",
  "special_features": None,
  "summary": None
} )
helpers[db.Inventory] = Helper( {
  "id": "id",
  "product_id": None,
  "date": "date",
  "normal_price": None,
  "discounted_price": None,
  "units": None,
  "note": None
} )
helpers[db.User] = Helper( {
  "id": "id",
  "name": None,
  "email": None,
  "groups": "multi"
} )
helpers[db.Ad] = Helper( {
  "id": "id",
  "name": None,
  "ad_type": "catalog",
  "content": None,
  "enabled": None,
  "valid_until": "date"
} )
helpers[db.Review] = Helper( {
  "id": "id",
  "product_id": None,
  "name": None,
  "alias": None,
  "date": "date",
  "rating": None,
  "content": None
} )
helpers[db.OrderDetail] = Helper( {
  "product": helpers[db.Product],
  "quantity": None,
  "cost": None
} )
helpers[db.Order] = Helper( {
  "id": "id",
  "user": helpers[db.User],
  "date": "date",
  "payment_type": None,
  "name": None,
  "country": None,
  "city": None,
  "state": None,
  "street": None,
  "postal_code": None,
  "total_amount": None,
  "payment_info": None,
  "detail": [helpers[db.OrderDetail]]
} )

def get( cls ):
  return helpers[cls]
