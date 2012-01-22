( function( $ ) {
  $.fn.hint = function( hint ) {
    return this.each( function() {
      var $this = $( this );
      $this.attr( "value", hint ).addClass( "hint" );
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

  $.forms = {};

  $.forms.multi_catalog = function ( field, catalog, hint ) {
    var $add = $( "#add_" + field );
    var $list = $( "#" + field );
    $add.hint( hint );
    $add.autocomplete( {
      source   : "find_in_catalog/?catalog_name=" + catalog,
      minLength: 2,
      select   : function( event, ui ) {
        if ( $( "#" + field + " option[value=" + ui.item.id + "]" ).length > 0 ) {
          alert( "Ese elemento ya está en la lista" );
        } else {
          $( "<option/>" ).attr( "value", ui.item.id ).text( ui.item.value ).appendTo( "#" + field );
        }
        ui.item.value = "";
      }
    } );

    var $last = null;

    $add.change( function( event ) {
      if ( $.trim( $add.attr( "value" ) ) != "" ) {
        $last = $( "<option/>" );
        $last.attr( "value", "*" ).text( this.value ).appendTo( "#" + field );
        $add.attr( "value", "" );
      } else {
        $last = null;
      }
    } );

    $add.keypress( function( event ) {
      $last = null;
    } );

    $add.blur( function( event ) {
      if ( $last != null ) {
        $last.remove();
      }
      $add.attr( "value", hint ).addClass( "hint" );
    } );

    $( "#remove_" + field ).click( function( event ) {
      event.preventDefault();
      $( "option:selected", $list ).remove();
    } );
  };

  $.forms.catalog = function ( field, catalog, hint ) {
    var $description = $( "#" + field );
    var $id  = $( "#" + field + "_id" );
    $description.hint( hint );
    $description.autocomplete( {
      source   : "find_in_catalog/?catalog_name=" + catalog,
      minLength: 2,
      select   : function( event, ui ) {
        $id.attr( "value", ui.item.id );
        $description.attr( "value", ui.item.value );
      }
    } );

    $description.change( function( event ) {
      if ( $.trim( $description.attr( "value" ) ) != "" ) {
        $id.attr( "value", "*" );
      }
    } );
  }
} )( jQuery );
