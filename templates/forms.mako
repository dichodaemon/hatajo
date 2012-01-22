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

<%def name="multi_catalog( field, label, catalog, hint )">
  <%core:add_code>
    $.forms.multi_catalog( "${field}", "${catalog}", "${hint}" )
  </%core:add_code>
  <%self:field field="${field}" label="${label}">
    <input name="add_${field}" id="add_${field}" type="text" value="" class="hint"/>
    <select id="${field}" multiple="1">
    </select>
    <button id="remove_${field}" class="button"/>Borrar</button>
    <div class="help">
      ${caller.body()}
    </div>
  </%self:field>
</%def>

<%def name="catalog( field, label, catalog, hint )">
  <%core:add_code>
    $.forms.catalog( "${field}", "${catalog}", "${hint}" )
  </%core:add_code>
  <%self:field field="${field}" label="${label}">
    <input id="${field}_id" type="hidden" value=""/>
    <input id="${field}" type="text"/>
    <div class="help">
      ${caller.body()}
    </div>
  </%self:field>
</%def>
