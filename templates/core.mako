<%def name="add_css( name )"><% _css.add( name ) %></%def>
<%def name="add_js( name )"><% _js.add( name ) %></%def>
<%def name="add_code()"><% 
  body = capture( caller.body ).rstrip()
  if not body in _code:
    _code.append( body ) 
%></%def>
