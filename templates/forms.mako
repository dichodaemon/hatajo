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

<%def name="multi_catalog( field, label, catalog, hint, tabindex=None )">
  <%core:add_code>
    $.forms.multi_catalog( "${field}", "${catalog}", "${hint}" );
    ${caller.body()}
  </%core:add_code>
  <%self:field field="${field}" label="${label}">
    %if tabindex != None:
    <input tabindex="${tabindex}" id="add_${field}" type="text" value="" class="hint"/>
    %else:
    <input id="add_${field}" type="text" value="" class="hint"/>
    %endif
    <select id="${field}" name="${field}" multiple="1">
    </select>
    <button id="remove_${field}" class="button"/>Borrar</button>
  </%self:field>
</%def>

<%def name="catalog( field, label, catalog, hint, tabindex=None )">
  <%core:add_code>
    $.forms.catalog( "${field}", "${catalog}", "${hint}" );
    ${caller.body()}
  </%core:add_code>
  <%self:field field="${field}" label="${label}">
    <input id="${field}_id" name="${field}_id" type="hidden" value=""/>
    %if tabindex != None:
    <input id="${field}" name="${field}" tabindex="${tabindex}" type="text"/>
    %else:
    <input id="${field}" name="${field}" type="text"/>
    %endif
  </%self:field>
</%def>

<%def name="text_field( field, label, hint, tabindex=None )">
  <%core:add_code>
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
