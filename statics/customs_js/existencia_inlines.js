/**
 * Created by eduardo on 22/11/16.
 */

$('.add_existencia_list').click(function () {
    //console.log("Pingaaaaaaaaaaaa");
    var reactivo_id = $(this).data("id");
    console.log("Pingaaaaaaaaaaaa " + reactivo_id);
    var count = $('#formset_existencia_' + reactivo_id + ' #forms_existencia_list_' + reactivo_id + ' >div').length;
    var panel = $("<div />", {'class': "panel panel-default", 'id': 'panel-existencia-' + count});

    // heading section
    var row_heading = $('<div />', {'class': "row"});
    var panel_heading = $("<div />", {'class': "panel-heading"});
    var col_label_heading = $("<div />", {'class': "col-xs-1"});
    var col_del_heading = $("<div />", {'class': "col-xs-2 pull-right"});

    col_del_heading.append($("<a />", {
        'class': 'btn btn-danger del_existencia_btn_list',
        'data-id': count,
        'data-reactivo': reactivo_id
    }).text(" Eliminar"));

    col_label_heading.append($('<h4 />').append($('<span />', {
        "class": "label",
        "text": "Existencia #" + (count + 1)
    })));
    row_heading.append(col_label_heading);
    row_heading.append(col_del_heading);
    panel_heading.append(row_heading);
    panel.append(panel_heading);

    //body section
    var table = $('<table />', {"class": "table"});
    var thead = $('<thead />');
    var tbody = $('<tbody />');

    var list_head = ["Cantidad", "Capacidad", "Unidad de Medida", "Tipo de envase", "Material del envase", "¿Es idoneo el almacenamiento?", "Firma"];

    var i = 0;
    while (i < list_head.length) {
        thead.append($("<th />").text(list_head[i]));
        i++;
    }

    table.append(thead);

    var table_tr = $('<tr />');
    var list_dict = [
        {
            "class": "form-control",
            "min": "0",
            "id": "id_existencias_" + reactivo_id + "-" + count + "-cantidad",
            "name": "existencias_" + reactivo_id + "-" + count + "-cantidad",
            "type": "number"
        },
        {
            "class": "form-control",
            "min": "0",
            "id": "id_existencias_" + reactivo_id + "-" + count + "-capacidad",
            "name": "existencias_" + reactivo_id + "-" + count + "-capacidad",
            "type": "number"
        },
        {
            "class": "form-control",
            "id": "id_existencias_" + reactivo_id + "-" + count + "-unidad_medida",
            "name": "existencias_" + reactivo_id + "-" + count + "-unidad_medida"
        },
        {
            "class": "form-control",
            "id": "id_existencias_" + reactivo_id + "-" + count + "-tipo_envase",
            "name": "existencias_" + reactivo_id + "-" + count + "-tipo_envase"
        },
        {
            "class": "form-control",
            "id": "id_existencias_" + reactivo_id + "-" + count + "-material_envase",
            "name": "existencias_" + reactivo_id + "-" + count + "-material_envase"
        },
        {
            "checked": "checked",
            "id": "id_existencias_" + reactivo_id + "-" + count + "-almacenamiento_idoneo",
            "name": "existencias_" + reactivo_id + "-" + count + "-almacenamiento_idoneo",
            "type": "checkbox"
        },
        {
            "class": "form-control",
            "id": "id_existencias_" + reactivo_id + "-" + count + "-firma",
            "name": "existencias_" + reactivo_id + "-" + count + "-firma",
            "maxlength": "100",
            "type": "text"
        }
    ];
    i = 0;
    var td;
    var select;

    var list_unidad_medida = ['mg', 'cg', 'dg', 'g', 'dag', 'hg', 'kg', 'lb', 'ml', 'cl', 'dl', 'litro', 'dal', 'hl', 'kl'];
    var list_material = ['Cristal', 'Metálico', 'Plástico', 'Cartón', 'Bolsa Multicapa'];
    var list_envase = ['Pomo', 'Caja', 'Tanque', 'Lata', 'Saco'];

    var j = 0;
    while (i < list_dict.length) {
        if (i >= 2 && i <= 4) {
            td = $('<td />');
            select = $('<select />', list_dict[i]);

            if (i == 2) {
                j = 0;
                while (j < list_unidad_medida.length) {
                    if (list_unidad_medida[j] == "g") {
                        select.append($("<option />", {
                            "value": list_unidad_medida[j],
                            "selected": "selected"
                        }).text(list_unidad_medida[j]));
                    } else {
                        select.append($("<option />", {
                            "value": list_unidad_medida[j]
                        }).text(list_unidad_medida[j]));
                    }
                    j++;
                }
            }
            if (i == 3) {
                j = 0;
                while (j < list_envase.length) {
                    if (list_envase[j] == "Pomo") {
                        select.append($("<option />", {
                            "value": list_envase[j],
                            "selected": "selected"
                        }).text(list_envase[j]));
                    } else {
                        select.append($("<option />", {
                            "value": list_envase[j]
                        }).text(list_envase[j]));
                    }
                    j++;
                }
            }
            if (i == 4) {
                j = 0;
                while (j < list_material.length) {
                    if (list_material[j] == "Cristal") {
                        select.append($("<option />", {
                            "value": list_material[j],
                            "selected": "selected"
                        }).text(list_material[j]));
                    } else {
                        select.append($("<option />", {
                            "value": list_material[j]
                        }).text(list_material[j]));
                    }
                    j++;
                }
            }
            td.append(select);
            table_tr.append(td);
        } else {
            table_tr.append($('<td />').append($('<input />', list_dict[i])));
        }
        i++;
    }

    tbody.append(table_tr);
    table.append(tbody);

    var panel_body = $("<div />", {'class': "panel-body"});
    var row_body = $("<div />", {"class": "row"});
    row_body.append(table);

    panel_body.append(row_body);
    panel.append(panel_body);

    $('#formset_existencia_' + reactivo_id + ' #forms_existencia_list_' + reactivo_id).append(panel);
    //$('#formset_list_'+reactivo_id+' #forms_sin_list_'+reactivo_id).append(row_form_button);
    $('#formset_existencia_' + reactivo_id + ' #id_existencias_' + reactivo_id + '-TOTAL_FORMS').val(parseInt(count) + 1);
});

$(document).on("click", ".del_existencia_btn_list", function () {
    var reactivo_id = $(this).data('reactivo');
    var id = $(this).data('id');
    var count = $('#formset_existencia_' + reactivo_id + ' #forms_existencia_list_' + reactivo_id + ' >div').length;

    $('#formset_existencia_' + reactivo_id + ' #forms_existencia_list_' + reactivo_id + ' >div').remove('#panel-existencia-' + id);

    var i = id + 1;
    while (i < count) {
        $('#formset_existencia_' + reactivo_id + ' #forms_existencia_list_' + reactivo_id + ' #panel-existencia-' + i + ' .panel-heading .row div h4 span').text("Existencia #" + i);
        $('#formset_existencia_' + reactivo_id + ' #forms_existencia_list_' + reactivo_id + ' #panel-existencia-' + i + ' .panel-heading .row div a').attr("data-id", (i - 1));
        $('#formset_existencia_' + reactivo_id + ' #forms_existencia_list_' + reactivo_id + ' #panel-existencia-' + i).attr("id", "panel-existencia-" + (i - 1));

        //$('#formset_existencia_' + reactivo_id + ' #forms_existencia_list_' + reactivo_id + ' #panel-existencia-' + i + ' .panel-body .row table tbody tr td #id_existencias_' + reactivo_id + "-" + i + "-cantidad")
        $('#id_existencias_' + reactivo_id + "-" + i + "-cantidad").attr({"id": '#id_existencias_' + reactivo_id + "-" + (i-1) + "-cantidad", "name": 'existencias_' + reactivo_id + "-" + (i-1) + "-cantidad"});
        $('#id_existencias_' + reactivo_id + "-" + i + "-capacidad").attr({"id": '#id_existencias_' + reactivo_id + "-" + (i-1) + "-capacidad", "name": 'existencias_' + reactivo_id + "-" + (i-1) + "-capacidad"});
        $('#id_existencias_' + reactivo_id + "-" + i + "-unidad_medida").attr({"id": '#id_existencias_' + reactivo_id + "-" + (i-1) + "-unidad_medida", "name": 'existencias_' + reactivo_id + "-" + (i-1) + "-unidad_medida"});
        $('#id_existencias_' + reactivo_id + "-" + i + "-tipo_envase").attr({"id": '#id_existencias_' + reactivo_id + "-" + (i-1) + "-tipo_envase", "name": 'existencias_' + reactivo_id + "-" + (i-1) + "-tipo_envase"});
        $('#id_existencias_' + reactivo_id + "-" + i + "-material_envase").attr({"id": '#id_existencias_' + reactivo_id + "-" + (i-1) + "-material_envase", "name": 'existencias_' + reactivo_id + "-" + (i-1) + "-material_envase"});
        $('#id_existencias_' + reactivo_id + "-" + i + "-almacenamiento_idoneo").attr({"id": '#id_existencias_' + reactivo_id + "-" + (i-1) + "-almacenamiento_idoneo", "name": 'existencias_' + reactivo_id + "-" + (i-1) + "-almacenamiento_idoneo"});
        $('#id_existencias_' + reactivo_id + "-" + i + "-firma").attr({"id": '#id_existencias_' + reactivo_id + "-" + (i-1) + "-firma", "name": 'existencias_' + reactivo_id + "-" + (i-1) + "-firma"});
        i++;
    }

    $('#formset_existencia_' + reactivo_id + ' #id_existencias_' + reactivo_id + '-TOTAL_FORMS').val(parseInt(count) - 1);
});
