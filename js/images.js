( function( $ ) {
  $.images = {};
  $.images.addItem = function ( field, value, key ) {
    var $list_item  = $( "<tr></tr>" ).hide();
    $( "#" + field + "__values" ).append( $list_item );
    var $td = $( "<td class='thumbnail'></td>" );
    $list_item.append( $td );
    var $imagea =  $( "<a href='/load_image?id=" + key + "' id=" + field + "__imga_" + key + "'></a>" );
    $imagea.append( $( "<img id='" + field + "__img_" + key + "' class='thumbnail'/>" ) );
    $imagea.imgPreview( {
      containerID: "imgPreviewWithStyles",
      onShow: function( link ) {
        $( link ).stop().animate( { opacity: 0.4 } );
        $( "img", this ).stop().css( { opacity: 0 } );
      },
      onLoad: function() {
        $( this ).animate( { opacity: 1 }, 300 );
      },
      onHide: function( link ) {
        $( link ).stop().animate( { opacity: 1 } );
      }
    } );
    $td.append( $imagea );
    $td = $( "<td class='checkbox'></td>" );
    $list_item.append( $td );
    $td.append( $( "<input type='checkbox' name='" + field + "__values' value='" + key + "'/><span>principal</span>" ) );
    $td.append( $( "<input type='hidden' name='" + field + "__ids' value='" + key + "'/>" ) );
    $td = $( "<td class='button'></td>" );
    $list_item.append( $td );
    var $button= $( "<button type='button'><img src='/img/list-remove.png'/></button>" );
    $td.append( $button );
    $button.click( function( event ) {$list_item.remove();} );
    $list_item.slideDown();
  }

  $.images.productImages = function ( field ) {
    var $add = $( "#add_" + field )[0];
    var $list = $( "#" + field + "__values" );

    var uploader = new qq.FileUploaderBasic( {
      button: $add,
      action: "upload_image", 
      sizeLimit: 1000000,
      allowedExtensions: ["png"],
      params: {}, 
      onComplete: function( id, fileName, id ) {
        $.images.addItem( field, false, id );
        $( "#" + field + "__img_" + id ).attr( "src", "/load_image?id=" + id );
      },
      messages: {
          typeError: "{file} es de un tipo inválido. Sólo {extensions} son permitidos.",
          sizeError: "{file} demasiado grande, no debe exceder {sizeLimit}.",
          minSizeError: "{file} demasiado pequeño, debe ser más de {minSizeLimit}.",
          emptyError: "{file} vacío, por favor verifíquelo.",
          onLeave: "Los archivos se están subiendo, si cierra ahora se interrumpirá."            
        },
    } );
  };

} )( jQuery );
