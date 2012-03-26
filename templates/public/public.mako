## -*- coding: utf-8 -*-
<%namespace name="core" file="/core.mako"/>
<%! import hatajo.webapp.template_helpers as h%>

<%def name="product( product )">
  <%core:add_code>
    $( "#r_${product["id"]}" ).ratings( ${int(product["review_avg"])}, false );
  </%core:add_code>
  <a href="/public/film_info?id=${product["id"]}"><img src="${h.main_image( product )}" class="main"/></a>
  <ul class="description">
    <li class="title"><a href="/public/film_info?id=${product["id"]}">${product["name"]}</a> (${( product["original_name"] + " " + str( product["year"] ) ).strip()})</li>
    <li>Director: ${", ".join( [d for d in product["directors"]["values"]] )} </li>
    <li>${", ".join( [a for a in product["actors"]["values"]] )}</li>
    <li><div id="r_${product["id"]}"></div> <a href="/public/product_reviews?id=${product["id"]}" class="ratings_count">${product["total_reviews"]} Comentarios</a></li>
    <li class="media">${", ".join( [a for a in product["medias"]["values"]] )}</li>
    <li class="price">Precio Normal <span class="normal">$${product["normal_price"]}</span> Precio de promoción <span class="discounted">$${product["discounted_price"]}</span></li>
    % if product["units"] > 0:
    <li class="delivery"><a href="/public/film_info?id=${product["id"]}">Ordena ahora y recíbela antes del ${h.next_date( 5 )}</a></li>
    % else:
    <li class="delivery"><a href="/public/film_info?id=${product["id"]}">Disponible en una semana</a></li>
    % endif
    % if product["units"] < 4 and product["units"] > 0:
    <li class="delivery"><a href="/public/film_info?id=${product["id"]}">Stock reducido ¡ordene pronto!</a></li>
    %endif
    <li class="special">Envío gratis en la compra de 3 películas</li>
  </ul>
</%def>

<%def name="pager()">
  <%core:add_js name="hint"/>
  <%core:add_code>
    function jump() {
      var filter = $( "#pager_filter" ).attr( "value" );
      var sort   = $( "#pager_sort" ).attr( "value" );
      var desc   = $( "#pager_descending" ).attr( "checked" );
      if ( $( "#pager_filter" ).hasClass( "hint" ) ) {
        filter = "";
      }
      if ( desc == undefined ) {
        desc = false;
      }
      var location = "${base_url}&filter=" + filter 
                   + "&sort_by=" + sort
                   + "&descending=" + desc;
      window.location = location
       
    };
    $( "#pager_filter" ).hint( "filtrar" );
    $( "#pager_filter" ).keypress( function( event ) {
      if ( event.keyCode == 13 ) {
        event.preventDefault();
        var filter = $.trim( $( this ).attr( "value" ) );
        jump();
        return false;
      }
    } );

    $( "#pager_sort" ).change( function() {
      jump();
    } );

    $( "#pager_descending" ).change( function() {
      jump();
    } );
  </%core:add_code>

  <div class="pager">
    <input id="pager_filter" type="text" class="search" value="${filter}"></input>
    <label for="pager_sort">Ordenar por</label>
    <select id="pager_sort" value="${sort_by}">
      % for f in sort_fields:
      % if sort_by == f[0]:
      <option value="${f[0]}" selected="true">${f[1]}</option>
      % else:
      <option value="${f[0]}">${f[1]}</option>
      % endif
      % endfor
    </select>
    <label for="pager_descending">Mayor a menor</label>
    % if not descending:
    <input id="pager_descending" type="checkbox" value="descending"/>
    % else:
    <input id="pager_descending" type="checkbox" value="descending" checked="1"/>
    % endif
  </div>
  ${caller.body()}
  <ul class="pager">
    % if page != 0:
    <li><a href="${base_url}&filter=${filter}&sort_by=${sort_by}&descending=${descending}&page=${page - 1}&limit=${limit}" class="previous">Anterior</a></li>
    % endif
    % for p in xrange( max( page - 5, 0 ), page ):
    <li><a href="${base_url}&filter=${filter}&sort_by=${sort_by}&descending=${descending}&page=${p}&limit=${limit}">${p + 1}</a></li>
    %endfor
    <li>${page + 1}</li>
    % for p in xrange( page + 1, min( page + 5, page_count ) ):
    <li><a href="${base_url}&filter=${filter}&sort_by=${sort_by}&descending=${descending}&page=${p}&limit=${limit}">${p + 1}</a></li>
    % endfor
    % if page < page_count -1:
    <li><a href="${base_url}&filter=${filter}&sort_by=${sort_by}&descending=${descending}&page=${page + 1}&limit=${limit}" class="next">Siguiente</a></li>
    % endif
  </ul>
</%def>

