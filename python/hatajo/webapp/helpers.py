import collections

def cleanup_arguments( args ):
  result = {}
  ids    = {}
  checks = []
  for key, value in args.items():
    if key.find( "__" ) == -1:
      #Normal fields
      result[key] = value
    else:
      #Special fields
      parts = key.split( "__" )
      field, field_type = parts[:2]
      args = parts[2:]

      if not field in result:
        result[field] = {}
      d = result[field]
      if field_type == "s":
        table, tag = args
        d[tag] = value
        d["table"] = table
      else:
        #Multiple fields
        if type( value ) != list:
          value = [value]
        if field_type == "m":
          table, tag = args
          d[tag] = value
          d["table"] = table
        if field_type == "i":
          if not "values" in d:
            d["values"] = []
            checks.append( ( field, "values" ) )
          tag = args[0]
          if tag == "ids":
            ids[field] = value
            d[tag] = value
          if tag == "values":
            d[tag] = set( value ) 
  for field, tag in checks:
    result[field][tag] = [id in result[field][tag] for id in ids[field]]

  return result

