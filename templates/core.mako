<%def name="add_css( name )"><% 
  if not name in _css:
    _css.append( name ) 
%></%def>
<%def name="add_js( name )"><% 
  if not name in _js:
    _js.append( name ) 
%></%def>
<%def name="add_code()"><% 
  body = capture( caller.body ).rstrip()
  if not body in _code:
    _code.append( body ) 
%></%def>
<%def name="add_head()"><% 
  body = capture( caller.body ).rstrip()
  if not body in _head:
    _head.append( body ) 
%></%def>
