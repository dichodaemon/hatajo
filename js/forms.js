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

  $.forms = {};
  $.forms.addItem = function ( field, value, key ) {
    var $list_item  = $( "<li></li>" ).hide();
    $( "#" + field + "__values" ).append( $list_item );
    $list_item.append( $( "<input type='text' readonly= '1' name='" + field + "__values' value='" + value + "'/>" ) );
    $list_item.append( $( "<input type='hidden' name='" + field + "__ids' value='" + key + "'/>" ) );
    var $button= $( "<button type='button'><img src='/img/list-remove.png'/></button>" );
    $list_item.append( $button );
    $button.click( function( event ) {$list_item.remove();} );
    $list_item.slideDown();
  }

  $.forms.multi_catalog = function ( field, hint ) {
    var $add = $( "#add_" + field );
    var $list = $( "#" + field + "__values" );
    $add.hint( hint );


    $add.autocomplete( {
      source   : "find_in_catalog/?catalog_name=" + field,
      minLength: 2,
      select   : function( event, ui ) {
        if ( $( "#" + field + "__values option[value=" + ui.item.id + "]" ).length > 0 ) {
          alert( "Ese elemento ya está en la lista" );
        } else {
          $.forms.addItem( field, ui.item.value, ui.item.id );
        }
        ui.item.value = "";
      }
    } );

    $add.blur( function( event ) {
      $add.attr( "value", hint ).addClass( "hint" );
    } );

    $add.keypress( function( event ) {
      if ( event.keyCode == 13 ) {
        event.preventDefault();
        if ( $.trim( $add.attr( "value" ) ) != "" ) {
          $.forms.addItem( field, $add.attr( "value" ), "new" );
          $add.attr( "value", "" );
        }
      }
    } );
  };

  $.forms.catalog = function ( field, hint ) {
    var $description = $( "#" + field + "__value" );
    var $id  = $( "#" + field + "__id" );
    $description.hint( hint );
    $description.autocomplete( {
      source   : "find_in_catalog/?catalog_name=" + field,
      minLength: 2,
      select   : function( event, ui ) {
        $id.attr( "value", ui.item.id );
        $description.attr( "value", ui.item.value );
      }
    } );

    $description.change( function( event ) {
      if ( $description.hasClass( "hint" ) ) {
        $id.attr( "value", "" );
      } else if (   $.trim( $description.attr( "value" ) ) != "" ) {
        $id.attr( "value", "new" );
      }
    } );
  }
} )( jQuery );
