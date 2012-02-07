def main_image( product ):
  for i in xrange( len( product["images"]["ids"] ) ):
    if product["images"]["values"][i]:
      return "/services/load_image?id=%i" % product["images"]["ids"][i]
  return "#"

def other_images( product ):
  result = []
  for i in xrange( len( product["images"]["ids"] ) ):
    if not product["images"]["values"][i]:
      result.append( product["images"]["ids"][i] )
  return result
