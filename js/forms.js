( function( $ ) {
  $.extend($.expr[':'], {
    data: function(elem, i, match) {
      return !!$.data(elem, match[3]);
    },

    focusable: function(element) {
      var nodeName = element.nodeName.toLowerCase();
      var tabIndex = $.attr(element, 'tabindex');
      return (/input|select|textarea|button|object/.test(nodeName)
        ? !element.disabled
        : 'a' == nodeName || 'area' == nodeName
          ? element.href || !isNaN(tabIndex)
          : !isNaN(tabIndex))
        // the element and all of its ancestors must be visible
        // the browser may report that the area is hidden
        && !$(element)['area' == nodeName ? 'parents' : 'closest'](':hidden').length;
    },

    tabbable: function(element) {
      var tabIndex = $.attr(element, 'tabindex');
      return (isNaN(tabIndex) || tabIndex >= 0) && $(element).is(':focusable');
    }
  });
  var tabables = null;

  $.fn.enter2tab = function() {
    return this.each( function() {
      $( this ).keydown( function( event ) {
        if ( event.keyCode == 13 ) {
          var current = tabables.index( this );
          var next = tabables.eq( current + 1 ).length ? tabables.eq( current + 1 ) : tabables.eq( 0 );
          next.focus();
          return false;
        }
      } );
    } );
  };


  $.fn.hintForm = function() {
    tabables = $( ":focusable" );
    return this.each( function() {
      $( this ).submit( function() {
        $( this ).find( "input.hint" ).each( function() {
          $( this ).attr( "value", "" );
        } );
        return true;
      } );
    } );
  };

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
  $.forms.addItem = function ( field, catalog, value, key ) {
    var prefix = field + "__m__" + catalog + "__";
    var $list_item  = $( "<li></li>" ).hide();
    $( "#" + field + "__values" ).append( $list_item );
    $list_item.append( $( "<input type='text' readonly= '1' name='" + prefix + "values' value='" + value + "'/>" ) );
    $list_item.append( $( "<input type='hidden' name='" + prefix + "ids' value='" + key + "'/>" ) );
    var $button= $( "<button type='button'><img src='/img/list-remove.png'/></button>" );
    $list_item.append( $button );
    $button.click( function( event ) {$list_item.remove();} );
    $list_item.slideDown();
  }

  $.forms.multi_catalog = function ( field, catalog, hint ) {
    var $add = $( "#add_" + field );
    var $list = $( "#" + field + "__values" );
    $add.hint( hint );

    $add.autocomplete( {
      source   : "/services/find_in_catalog/?catalog_name=" + catalog,
      minLength: 2,
      select   : function( event, ui ) {
        if ( $( "#" + field + "__values option[value=" + ui.item.id + "]" ).length > 0 ) {
          alert( "Ese elemento ya está en la lista" );
        } else {
          $.forms.addItem( field, catalog, ui.item.value, ui.item.id );
        }
        ui.item.value = "";
      }
    } );

    $add.blur( function( event ) {
      $add.attr( "value", hint ).addClass( "hint" );
    } );

    var current = tabables.index( $add );
    var next = !!tabables.eq( current + 1 ).length ? tabables.eq( current + 1 ) : tabables.eq( 0 );

    $add.keypress( function( event ) {
      if ( event.keyCode == 13 ) {
        event.preventDefault();
        if ( $.trim( $add.attr( "value" ) ) != "" ) {
          $.forms.addItem( field, catalog, $add.attr( "value" ), "new" );
          $add.attr( "value", "" );
        } else {
          next.focus();
        }
        return false;
      }
    } );
  };

  $.forms.catalog = function ( field, catalog, hint ) {
    var prefix = field + "__s__" + catalog + "__";
    var $description = $( "#" + prefix + "value" );
    var $id  = $( "#" + prefix + "id" );
    $description.hint( hint );
    $description.enter2tab();
    $description.autocomplete( {
      source   : "/services/find_in_catalog/?catalog_name=" + catalog,
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
