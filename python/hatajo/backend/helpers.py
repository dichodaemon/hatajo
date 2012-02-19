# -*- coding: utf-8 -*-

import db
from helper import Helper, main_form

helpers = {
  db.Product: Helper( {
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
    "studio": "catalog",
    "duration": None,
    "rtc": None,
    "bar_code": None,
    "images": "images",
    "special_features": None,
    "summary": None
  } ),
  db.Ad: Helper( {
    "id": "id",
    "name": None,
    "ad_type": "catalog",
    "content": None,
    "enabled": None,
    "valid_until": "date"
  } )
}

def get( cls ):
  return helpers[cls]
