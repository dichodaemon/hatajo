## -*- coding: utf-8 -*-
<%namespace name="core" file="/core.mako"/>
<%namespace name="ratings" file="/ratings.mako"/>
<%! import hatajo.webapp.template_helpers as h %>

<%def name="review_summary( product, reviews )">
  <%
    total_reviews, review_avg, reviews_by_rating = h.review_stats( reviews )
  %>
  <%core:add_code>
    % for i in xrange( 1, 6 ):
    % if total_reviews > 0:
    $( "#${i}_stars" ).width( ${int( 100 * reviews_by_rating[i] / total_reviews )} );
    % else:
    $( "#${i}_stars" ).width( 0 );
    % endif
    % endfor
  </%core:add_code>
  ${ratings.show_rating( "#ratings_%i" % product["id"], review_avg )}

  <h2>Comentarios de los usuarios:</h2>
  % if len( reviews ) > 0:
  <ul class="rating_list">
    <li><a href="#">5 estrellas</a><div class="bar_outer"><div id="5_stars" class="bar_inner"></div></div>(${reviews_by_rating[5]}) <div id="ratings_${product["id"]}"></div> en ${total_reviews} comentarios</li>
    <li><a href="#">4 estrellas</a><div class="bar_outer"><div id="4_stars" class="bar_inner"></div></div>(${reviews_by_rating[4]})</li>
    <li><a href="#">3 estrellas</a><div class="bar_outer"><div id="3_stars" class="bar_inner"></div></div>(${reviews_by_rating[3]})</li>
    <li><a href="#">2 estrellas</a><div class="bar_outer"><div id="2_stars" class="bar_inner"></div></div>(${reviews_by_rating[2]})</li>
    <li><a href="#">1 estrellas</a><div class="bar_outer"><div id="1_stars" class="bar_inner"></div></div>(${reviews_by_rating[1]})</li>
  </ul>
  % else:
  <p class="rating_list">Ningún usuario ha comentado este producto ¡sea el primero en hacerlo!</p>
  % endif
  <div class="add_review">
    <p>Comparta sus ideas con otros clientes:</p>
    <p><a href="/public/review_edit?product_id=${product["id"]}">Crear comentario</a></p>
  </div>
</%def>

<%def name="review_details( review, product )">
  ${ratings.show_rating( "#review_" + str( review["id"] ), review["rating"] )}
  <h1><span id="review_${review["id"]}" class="rating_container"></span> <span class="title">${review["name"]}</span></h1>
  <h2>Escrito por <span class="user">${review["alias"]}</span> el <span class="date">${review["date"]}</span></h2>
  <h3>Comentario acerca de: <span class="name">${product["name"]}</span></h3>
  <div class="content">
    <p>
    ${"</p><p>".join( review["content"].split( "\n" ) )}
    </p>
  </div>
</%def>
