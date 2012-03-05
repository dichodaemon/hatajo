# -*- coding: utf-8 -*-

from helper import Helper

def review_stats( reviews ):
  total_reviews = len( reviews )
  if total_reviews > 0:
    review_avg = sum( [r.rating for r in reviews] ) / total_reviews
  else:
    review_avg = 3
  reviews_by_rating = [0] * 6
  for r in reviews:
    reviews_by_rating[int( r.rating )] += 1
  return total_reviews, review_avg, reviews_by_rating

class ProductHelper( Helper ):
  def __init__( self, fields ):
    Helper.__init__( self, fields )

  def to_dictionary( self, record ):
    d = Helper.to_dictionary( self, record )
    total_reviews, review_avg, reviews_by_rating = review_stats( record.reviews )
    d["total_reviews"] = total_reviews
    d["review_avg"] = review_avg
    d["reviews_by_rating"] = reviews_by_rating
    return d

