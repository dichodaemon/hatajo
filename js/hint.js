( function( $ ) {
  $.fn.hint = function( hint ) {
    return this.each( function() {
      var $this = $( this );
      if ( $this.attr( "value" ) == hint 
        || $.trim( $this.attr( "value" ) ) == "" 
      ) {
        $this.attr( "value", hint ).addClass( "hint" );
      }

      $this.change( function( event ) {
        if ( $.trim( $this.attr( "value" ) ) != "" ) {
          $this.removeClass( "hint" );
        } else {
          $this.attr( "value", hint ).addClass( "hint" );
        }
      } );

      $this.focus( function() {
        if ( $this.hasClass( "hint" ) ) {
          $this.removeClass( "hint" );
          $this.attr( "value", "" );
        }
      } );

      $this.blur( function() {
        if ( $.trim( $this.attr( "value" ) ) == "" ) {
          $this.attr( "value", hint ).addClass( "hint" );
        }
      } );

      $this.keypress( function() {
        if ( $this.hasClass( "hint" ) ) {
          $this.removeClass( "hint" );
          $this.attr( "value", "" );
        }
      } );
    } );
  };
} )( jQuery );
