( function( $ ) {
  $.fn.ratings = function( value, edit ) {
    return this.each( function() {
      var container = $( this );
      initContainer( container, edit );
      updateRatings( container, value );
      if ( edit ) {
        $( "span", $( this ) ).each( function() {
          var $span = $( this );
          $span.click( function() {
            updateRatings( container, parseFloat( $span.attr( "rel" ) ) );
          } );    
        } );
      }
    } );
  }
  
  function initContainer( container, edit )
  {
    container.addClass( "ratings" );
    if ( edit ) {
      container.addClass( "ratings_edit" );
    }
    for ( var i = 1; i < 6; i++ ) {
      var span = jQuery( "<span class='undone' rel='" + i + "'>*</span>" )
      .appendTo( container );
      if ( edit ) {
        $( span ).addClass( "edit" );
      }
    }
  }

  function updateRatings( container, value ) 
  {
    container.find( "span" ).each( function( i ) {
      if ( parseFloat( $( this ).attr( "rel" ) ) <= value ) {
        $( this ).attr( { "class": "done" } );
      } else {
        $( this ).attr( { "class": "undone" } );
      }
    } );
  }
  
} )( jQuery );
