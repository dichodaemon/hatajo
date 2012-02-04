CKEDITOR.editorConfig = function( config )
{
  config.language = "es";
  config.toolbar_Hatajo = [	
    { name: 'document', items : [ "Source" ] },
    { name: 'clipboard', items: [ "Cut", "Copy", "Paste", 'PasteText', 'PasteFromWord', "-", "Undo", "Redo" ] },
    { name: 'insertNodert', items : [ 'Image','Table','HorizontalRule','Smiley','SpecialChar'] },
    { name: 'basicstyles', items : [ 'Bold','Italic','Underline','Strike','Subscript','Superscript','-','RemoveFormat' ] },
    { name: 'links', items : [ 'Link','Unlink','Anchor' ] },
    { name: 'paragraph', items : [ 'NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote','CreateDiv','-',
                                   'JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock','-','BidiLtr','BidiRtl' ] },
  ];
  config.toolbar  = "Hatajo";
  config.filebrowserUploadUrl = "/ck_upload_image";
};
