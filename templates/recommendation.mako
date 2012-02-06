## -*- coding: utf-8 -*-
<%namespace name="core" file="core.mako"/>
<%!
count = 0
def main_image( product ):
  for i in xrange( len( product["images"]["ids"] ) ):
    if product["images"]["values"][i]:
      return "/load_image?id=%i" % product["images"]["ids"][i]
  return "#"
%>

<%def name="recommendation( title, method )">
  <% global count %>
  <%core:add_css name="recommendations"/>
  <%core:add_code>
    $( "#recommendation_${count}" ).load( "/recommendation?title=${title | u}&method=${method | u}" )
    ${caller.body()}
  </%core:add_code>
  <div id="recommendation_${count}"></div>
  <%count += 1 %>
</%def>
