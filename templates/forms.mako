## -*- coding: utf-8 -*-
<%namespace name="core" file="core.mako"/>
<%!
def q( text ):
  return text.replace( "\"", "\\\"" )
%>
<%def name="form( action, method )">
  <%core:add_js name="forms"/>
  <%core:add_code>
    $( "form.main_form" ).hintForm();
    //$( "form.main_form:focusable" ).first().focus();
  </%core:add_code>
  <form class="main_form" action="${action}" method="${method}">
  ${caller.body()}
  </form>
</%def>

<%def name="field( field, label )">
  %if field in errors or field in warnings:
  <tr id="${field}_row" class="field error">
  %else:
  <tr id="${field}_row" class="field">
  %endif
    <td class="label">
      <label for="${field}">${label}</label>
    </td>
    <td class="field">
      ${caller.body()}
      %if field in errors:
      <ul class="error">
      %for e in errors[field]:
        <li>${e}</li>
      %endfor
      </ul>
      %endif
    </td>
  </tr>
</%def>

<%def name="multi_catalog( field, catalog, label, hint, tabindex=None )">
  <%core:add_js name="jquery-ui-1.8.17.custom.min"/>
  <%core:add_js name="forms"/>
  <%core:add_code>
    $.forms.multi_catalog( "${field}", "${catalog}", "${hint}" );
    %if field in data:
    %for i in xrange( len( data[field]['ids'] ) ):
    $.forms.addItem( "${field}", "${catalog}", "${data[field]['values'][i] | q}", "${data[field]['ids'][i]}" );
    %endfor  
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

<%def name="catalog( field, catalog, label, hint, tabindex=None )">
  <% prefix = field + "__s__" + catalog + "__" %> 
  <%core:add_js name="jquery-ui-1.8.17.custom.min"/>
  <%core:add_js name="forms"/>
  <%core:add_code>
    %if field in data:
    $( "#${prefix}value" ).attr( "value", "${data[field]['value'] | q}" );
    $( "#${prefix}id" ).attr( "value", "${data[field]['id']}" );
    %endif
    $.forms.catalog( "${field}", "${catalog}", "${hint}" );
    ${caller.body()}
  </%core:add_code>
  <%self:field field="${field}" label="${label}">
    <input id="${prefix}id" name="${prefix}id" type="hidden" value=""/>
    %if tabindex != None:
    <input id="${prefix}value" name="${prefix}value" tabindex="${tabindex}" type="text"/>
    %else:
    <input id="${prefix}value" name="${prefix}value" type="text"/>
    %endif
  </%self:field>
</%def>

<%def name="text_field( field, label, hint, tabindex=None )">
  <%core:add_code>
    %if field in data:
    $( "#${field}" ).attr( "value", "${context[field] | q}" );
    %endif
    $( "#${field}" ).hint( "${hint}" ).enter2tab();
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
    ${caller.body()}
  </%core:add_code>
  <%self:field field="${field}" label="${label}">
    %if tabindex != None:
    <textarea id="${field}" name="${field}" tabindex="${tabindex}">${context.get( field, "" ) | h}</textarea>
    %else:
    <textarea id="${field}" name="${field}">${context.get( field, "" ) | h}</textarea>
    %endif
  </%self:field>
</%def>

<%def name="images( field, label, hint, tabindex=None )">
  <%core:add_js name="jquery-ui-1.8.17.custom.min"/>
  <%core:add_js name="fileuploader"/>
  <%core:add_js name="images"/>
  <%core:add_js name="imgpreview.full.jquery"/>
  <%core:add_code>
    $.images.productImages( "${field}", "${hint}" );
    %if field in data:
    %for i in xrange( len( data[field]['ids'] ) ):
    %if "values" in data[field]:
    $.images.addItem( "${field}", "${data[field]['values'][i] | q}", "${data[field]['ids'][i]}" );
    %else:
    $.images.addItem( "${field}", "False", "${data[field]['ids'][i]}" );
    %endif
    %endfor  
    %endif
    $( "#add_${field}" ).enter2tab();
    ${caller.body()}
  </%core:add_code>
  <%self:field
    field="${field}"
    label="${label}">
    %if tabindex != None:
    <button id="add_${field}" class="images" tabindex="${tabindex}">        
    %else:
    <button id="add_${field}" class="images">        
    %endif
      Subir imágenes
    </button>
    <table id="${field}__values" class="images">
    </table>
    </ul>
  </%self:field>
</%def>
