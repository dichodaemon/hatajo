( function( $ ) {
  $.fn.table = function( options ) {
    var opts = $.extend( {}, $.fn.table.defaults, options );
    return this.each( function() {
      var table = $( this );
      var tableOptions = $.extend( {}, $.fn.table.tableDefaults, options.tableOptions );
      table.dataTable( tableOptions );
      var dataTable = table.dataTable();
      $( "div.toolbar" ).append( $( opts.menu ) );
      table.find( "tbody tr" ).live( "click", function( e ) {
        table.find( "tr.selected" ).removeClass( "selected" );
        $( this ).addClass( "selected" );
      } );
    } );
  };
  $.fn.selectedRow = function() {
    var selected = $( this ).find( "tr.selected" );
    if ( selected.length == 0 ) {
      return null;
    } else {
      return selected.first();
    }
  };

  $.fn.table.defaults = {
  };

  $.fn.table.tableDefaults = {
    "bProcessing": true,
    "bServerSide": true,
    "oLanguage": 
      {
        "sSearch"      : "Buscar",
        "sLengthMenu"  : "Mostrar _MENU_ elementos",
        "sZeroRecords" : "Lo siento, no hay elementos correspondientes",
        "sInfo"        : "Mostrando de _START_ a _END_ de _TOTAL_ elementos",
        "sInfoEmpty"   : "Mostrando 0 elementos",
        "sInfoFiltered": ""
    },
    "sDom": 'frl<"clear"><"toolbar">tip'
  }
} ) ( jQuery );

