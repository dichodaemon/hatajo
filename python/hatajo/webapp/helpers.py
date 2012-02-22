import collections

def cleanup_arguments( args ):
  result = {}
  ids    = {}
  checks = []
  for key, value in args.items():
    if type( value ) == str:
      value = value.strip()
    if key.find( "__" ) == -1:
      #Normal fields
      result[key] = value
    else:
      #Special fields
      parts = key.split( "__" )
      field, field_type = parts[:2]
      args = parts[2:]
      print field, field_type

      if field_type == "c":
        print field
        result[field] = value == "on"
        continue
      if not field in result:
        result[field] = {}
      d = result[field]
      if field_type == "s":
        table, tag = args
        if not "value" in d:
          d["value"] = ""
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

def pager_helper( 
  call, id=None, filter="", sort_by="date", 
  descending=True, offset=0, limit=10
):
  if type( descending ) in [unicode, str]:
    descending = descending == "checked"
  if type( filter ) == int:
    filter = ""
  offset = int( offset )
  limit = int( limit )
  content, page_count = call( symbol, filter, sort_by, descending, offset, limit )
  return {
    "page_count": page_count,
    "offset": offset,
    "articles": articles,
    "filter": filter,
    "sort_by": sort_by,
    "descending": descending,
    "limit": limit, 
    "date": date
  }

def datatable_helper(
    backend, table, filter_field, sort_columns, **kargs 
) :
  filter = "sSearch" in kargs and kargs["sSearch"] or ""
  offset = "iDisplayStart" in kargs and int( kargs["iDisplayStart"] ) or 0
  limit  = "iDisplayLength" in kargs and int( kargs["iDisplayLength"] ) or 0
  sort_column = "iSortCol_0" in kargs and int( kargs["iSortCol_0"] ) or 0
  sort_by = sort_columns[sort_column]
  descending  = not ( "sSortDir_0" in kargs and kargs["sSortDir_0"] == "asc" )
  data, total_records = backend.pager( table, filter_field, filter, sort_by, descending, offset, limit )
  return {
    "sEcho": kargs["sEcho"],
    "iTotalRecords": total_records,
    "iTotalDisplayRecords": total_records,
    "aaData": data 
  }
