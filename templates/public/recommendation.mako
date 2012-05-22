## -*- coding: utf-8 -*-
<%namespace name="core" file="/core.mako"/>
<%!
count = 0
%>

<%def name="recommendation( title, method, layout='horizontal' )">
  <% global count %>
  <%core:add_css name="public/recommendations"/>
  <%core:add_code>
    $( "#recommendation_${count}" ).load( "/public/recommendation?layout=${layout}&title=${title | u}&method=${method | u}" );
    ${caller.body()}
  </%core:add_code>
  <div id="recommendation_${count}"></div>
  <%count += 1 %>
</%def>
