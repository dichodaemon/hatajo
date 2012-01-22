<%def name="add_css( name )"><% 
  if not name in _code:
    _css.append( name ) 
%></%def>
<%def name="add_js( name )"><% 
  if not name in _code:
    _js.append( name ) 
%></%def>
<%def name="add_code()"><% 
  body = capture( caller.body ).rstrip()
  if not body in _code:
    _code.append( body ) 
%></%def>
