## -*- coding: utf-8 -*-
<%namespace name="core" file="/core.mako"/>
<%namespace name="ratings" file="/ratings.mako"/>
<%! import hatajo.webapp.template_helpers as h %>

<%def name="review_summary( product, reviews )">
  <%core:add_code>
    % for i in xrange( 1, 6 ):
    % if product["total_reviews"] > 0:
    $( "#${i}_stars" ).width( ${int( 100 * product["reviews_by_rating"][i] / product["total_reviews"] )} );
    % else:
    $( "#${i}_stars" ).width( 0 );
    % endif
    % endfor
  </%core:add_code>
  ${ratings.show_rating( "#ratings_%i" % product["id"], product["review_avg"] )}

  <h2>Comentarios de los usuarios:</h2>
  % if ( product["total_reviews"] ) > 0:
  <ul class="rating_list">
    <li><a href="/public/product_reviews?id=${product["id"]}&rating=5">5 estrellas</a><div class="bar_outer"><div id="5_stars" class="bar_inner"></div></div>(${product["reviews_by_rating"][5]}) <div id="ratings_${product["id"]}"></div> en ${product["total_reviews"]} comentarios</li>
    <li><a href="/public/product_reviews?id=${product["id"]}&rating=4">4 estrellas</a><div class="bar_outer"><div id="4_stars" class="bar_inner"></div></div>(${product["reviews_by_rating"][4]})</li>
    <li><a href="/public/product_reviews?id=${product["id"]}&rating=3">3 estrellas</a><div class="bar_outer"><div id="3_stars" class="bar_inner"></div></div>(${product["reviews_by_rating"][3]})</li>
    <li><a href="/public/product_reviews?id=${product["id"]}&rating=2">2 estrellas</a><div class="bar_outer"><div id="2_stars" class="bar_inner"></div></div>(${product["reviews_by_rating"][2]})</li>
    <li><a href="/public/product_reviews?id=${product["id"]}&rating=1">1 estrellas</a><div class="bar_outer"><div id="1_stars" class="bar_inner"></div></div>(${product["reviews_by_rating"][1]})</li>
  </ul>
  % else:
  <p class="rating_list">Ningún usuario ha comentado este producto ¡sea el primero en hacerlo!</p>
  % endif
  <div class="add_review">
    <p>Comparta sus ideas con otros usuarios:</p>
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
