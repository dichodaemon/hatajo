def review_stats( reviews ):
  total_reviews = len( reviews )
  if total_reviews > 0:
    review_avg = sum( [c["rating"] for c in reviews] ) / total_reviews
  else:
    review_avg = 3
  reviews_by_rating = [0] * 6
  for r in reviews:
    reviews_by_rating[int( r["rating"] )] += 1
  return total_reviews, review_avg, reviews_by_rating

