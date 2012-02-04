## -*- coding: utf-8 -*-
<%namespace name="core" file="core.mako"/>

<%def name="field( field, label )">
  <tr id="${field}_row" class="field">
    <td class="label">
      <label for="${field}">${label}</label>
    </td>
    <td class="field">
      ${caller.body()}
    </td>
  </tr>
</%def>

<%def name="multi_catalog( field, label, hint, tabindex=None )">
  <%core:add_css name="custom-theme/jquery-ui-1.8.17.custom"/>
  <%core:add_css name="forms"/>
  <%core:add_js name="jquery-ui-1.8.17.custom.min"/>
  <%core:add_js name="forms"/>
  <%core:add_code>
    $.forms.multi_catalog( "${field}", "${hint}" );<%fields = context.get( field + "__values", [] )%>
    %if type( fields ) == list:
    %for i in xrange( len( fields ) ):
    $.forms.addItem( "${field}", "${context[field + '__values'][i]}", "${context[field + '__ids'][i]}" );
    %endfor  
    %else:
    $.forms.addItem( "${field}", "${context[field + '__values']}", "${context[field + '__ids']}" );
    %endif
    ${caller.body()}
  </%core:add_code>
  <%self:field field="${field}" label="${label}">
    %if tabindex != None:
    <input tabindex="${tabindex}" id="add_${field}" type="text" value="" class="hint"/>
    %else:
    <input id="add_${field}" type="text" value="" class="hint"/>
    %endif
    <ul id="${field}__values" class="items">
    </ul>
  </%self:field>
</%def>

<%def name="catalog( field, label, hint, tabindex=None )">
  <%core:add_css name="custom-theme/jquery-ui-1.8.17.custom"/>
  <%core:add_css name="forms"/>
  <%core:add_js name="jquery-ui-1.8.17.custom.min"/>
  <%core:add_js name="forms"/>
  <%core:add_code>
    %if context.get( field + "__id", False ):
    $( "#${field}__value" ).attr( "value", "${context[field + '__value']}" );
    $( "#${field}__id" ).attr( "value", "${context[field + '__id']}" );
    %endif
    $.forms.catalog( "${field}", "${hint}" );
    ${caller.body()}
  </%core:add_code>
  <%self:field field="${field}" label="${label}">
    <input id="${field}__id" name="${field}__id" type="hidden" value=""/>
    %if tabindex != None:
    <input id="${field}__value" name="${field}__value" tabindex="${tabindex}" type="text"/>
    %else:
    <input id="${field}__value" name="${field}__value" type="text"/>
    %endif
  </%self:field>
</%def>

<%def name="text_field( field, label, hint, tabindex=None )">
  <%core:add_code>
    %if context.get( field, False ):
    $( "#${field}" ).attr( "value", "${context[field]}" );
    %endif
    $( "#${field}" ).hint( "${hint}" );
    ${caller.body()}
  </%core:add_code>
  <%self:field field="${field}" label="${label}">
    %if tabindex != None:
    <input id="${field}" name="${field}" tabindex="${tabindex}" type="text"/>
    %else:
    <input id="${field}" name="${field}" type="text"/>
    %endif
  </%self:field>
</%def>

<%def name="rich_text( field, label, tabindex=None )">
  <%core:add_head>
    <script type="text/javascript" src="/ckeditor/ckeditor.js"></script>
    <script type="text/javascript" src="/ckeditor/adapters/jquery.js"></script>
  </%core:add_head>
  <%core:add_code>
    $( "#${field}" ).ckeditor();
  </%core:add_code>
  <%self:field field="${field}" label="${label}">
    %if tabindex != None:
    <textarea id="${field}" name="${field}" tabindex="${tabindex}">
    </textarea>
    %else:
    <textarea id="${field}" name="${field}">
    </textarea>
    %endif
  </%self:field>
</%def>

<%def name="images( field, label, hint, tabindex=None )">
  <%core:add_css name="forms"/>
  <%core:add_js name="jquery-ui-1.8.17.custom.min"/>
  <%core:add_js name="fileuploader"/>
  <%core:add_js name="images"/>
  <%core:add_js name="imgpreview.full.jquery"/>
  <%core:add_code>
    $.images.productImages( "${field}", "${hint}" );
  </%core:add_code>
  <%self:field
    field="${field}"
    label="${label}">
    <button id="add_${field}" class="images" tabindex="${tabindex}">        
      Subir imágenes
    </button>
    <table id="${field}__values" class="images">
    </table>
    </ul>
  </%self:field>
</%def>
