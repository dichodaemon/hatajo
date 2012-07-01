import datetime

months = ["Enero", "Febrero", "Marzo", "Abril", "Junio", "Julio", "Agosto", 
          "Septiembre", "Octubre", "Noviembre", "Diciembre"]

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

def next_date( days, date=None ):
  if date == None:
    date = datetime.datetime.now()
  elif type( date ) == str:
    date = datetime.datetime.strptime( date, "%d/%m/%Y" )
  date = date + datetime.timedelta( days = days )
  return "%i de %s" % ( date.day, months[date.month - 1] )


