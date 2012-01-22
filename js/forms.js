( function( $ ) {
  $.forms = {};

  $.forms.multi_catalog = function ( field, catalog, hint ) {
    var $add = $( "#add_" + field );
    var $list = $( "#" + field );
    $add.attr( "value", hint ).addClass( "hint" );
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

    $add.change( function( event ) {
      if ( $.trim( $add.attr( "value" ) ) != "" ) {
        $( "<option/>" ).attr( "value", "" ).text( this.value ).appendTo( "#" + field );
      }
      $add.attr( "value", hint ).addClass( "hint" );
    } );

    $add.focus( function() {
      if ( $add.hasClass( "hint" ) ) {
        $add.removeClass( "hint" );
        $add.attr( "value", "" );
      }
    } );

    $add.blur( function() {
      if ( $.trim( $add.attr( "value" ) ) == "" ) {
        $add.attr( "value", hint ).addClass( "hint" );
      }
    } );

    $add.keypress( function() {
      if ( $add.hasClass( "hint" ) ) {
        $add.removeClass( "hint" );
        $add.attr( "value", "" );
      }
    } );

    $( "#remove_" + field ).click( function( event ) {
      event.preventDefault();
      $( "option:selected", $list ).remove();
    } );
  };

  $.forms.catalog = function ( field, catalog, hint ) {
    var $description = $( "#" + field );
    var $id  = $( "#" + field + "_id" );
    $description.attr( "value", hint ).addClass( "hint" );
    $description.autocomplete( {
      source   : "find_in_catalog/?catalog_name=" + catalog,
      minLength: 2,
      select   : function( event, ui ) {
        $id.attr( "value", ui.item.id );
        $description.attr( "value", ui.item.value );
      }
    } );

    $description.change( function( event ) {
      if ( $.trim( $description.attr( "value" ) ) == "" ) {
        $description.attr( "value", "" );
      }
    } );

    $description.focus( function() {
      if ( $description.hasClass( "hint" ) ) {
        $description.removeClass( "hint" );
        $description.attr( "value", "" );
      }
    } );

    $description.blur( function() {
      if ( $.trim( $description.attr( "value" ) ) == "" ) {
        $description.attr( "value", hint ).addClass( "hint" );
      }
    } );

    $description.keypress( function() {
      if ( $description.hasClass( "hint" ) ) {
        $description.removeClass( "hint" );
        $description.attr( "value", "" );
      }
    } );
  }
} )( jQuery );
