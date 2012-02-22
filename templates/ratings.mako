## -*- coding: utf-8 -*-
<%namespace name="core" file="core.mako"/>
<%namespace name="forms" file="forms.mako"/>

<%def name="rating( field, label )">
  <%core:add_js name="ratings"/>
  <%core:add_code>
    % if field in data:
    $( "#${field}__ranking" ).ratings( ${data[field]}, true, "#${field}" );
    % else:
    $( "#${field}__ranking" ).ratings( 3, true, "#${field}" );
    % endif
  </%core:add_code>
  <%forms:field field="${field}" label="${label}">
    <span id="${field}__ranking"></span>
    <input type="hidden" id="${field}" name="${field}"/>
  </%forms:field>
</%def>

<%def name="show_rating( span, value )">
  <%core:add_js name="ratings"/>
  <%core:add_code>
    $( "${span}" ).ratings( ${value}, false );
  </%core:add_code>
</%def>


