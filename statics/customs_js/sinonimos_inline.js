/**
 * Created by eduardo on 16/11/16.
 */

$('#add_more_add').click(function () {
    //console.log("Pingaaaaaaaaaaaa");
    var count = $('#formset_add #forms_sin_add >div').length / 2;
    var row_label = $("<div />", {'class': "row", 'id': 'label_sin_' + count});
    var row_form = $("<div />", {'class': "row", 'id': 'input_sin_' + count});


    var h4 = $("<h4 />", {'id': "id_nombre_frasco"});

    console.log(count);
    var span_label = $("<span />", {'class': "label"}).text("Sinonimo #" + (parseInt(count) + 1) + ":");

    var input = $('<input />', {
        'id': 'id_sinonimos-' + count + '-sinonimo',
        'class': 'form-control',
        'maxlength': "150",
        "type": "text",
        "name": 'sinonimos-' + count + '-sinonimo'
    });

    row_form.append($("<div />", {'class': "col-xs-11"}).append(input));
    var row_form_button = row_form.append($("<div />", {'class': "col-xs-1"}).append($("<a />", {
        'class': 'btn btn-danger del_sin_btn',
        'data-id': count
    }).text(" Eliminar")));

    $('#formset_add #forms_sin_add').append(row_label.append(h4.append(span_label)));
    $('#formset_add #forms_sin_add').append(row_form_button);
    $('#formset_add #id_sinonimos-TOTAL_FORMS').val(parseInt(count) + 1);
});

$(document).on("click", ".del_sin_btn", function () {
    var count = $('#formset_add #forms_sin_add >div').length / 2;
    var id = $(this).data('id');

    console.log("Heyyyyyyyyyyyyyyyy " + id);
    $('#formset_add #forms_sin_add >div').remove('#label_sin_' + id);
    $('#formset_add #forms_sin_add >div').remove('#input_sin_' + id);

    var i = id + 1;
    while (i < count) {
        $('#formset_add #forms_sin_add #label_sin_' + i + ' h4 span').text("Sinonimo #" + (i) + ":");
        $('#formset_add #forms_sin_add #label_sin_' + i).attr("id","label_sin_" + (i-1));
        $('#formset_add #forms_sin_add #input_sin_' + i).attr("id","input_sin_" + (i-1));
        $('#formset_add #forms_sin_add #input_sin_' + (i-1) + ' div input').attr({"id":"id_sinonimos-" + (i-1) + "-sinonimo", "name": "sinonimos-" + (i-1) + "-sinonimo"});
        $('#formset_add #forms_sin_add #input_sin_' + (i-1) + ' div a').attr("data-id", (i-1));
        console.log("current id "+i);
        i++;
    }

    $('#formset_add #id_sinonimos-TOTAL_FORMS').val(parseInt(count) - 1);
});

$('.add_more_list').click(function () {
    //console.log("Pingaaaaaaaaaaaa");
    var reactivo_id = $(this).data('id');
    console.log("Pingaaaaaaaaaaaa "+reactivo_id);
    var count = $('#formset_list_'+reactivo_id+' #forms_sin_list_'+reactivo_id+' >div').length / 2;
    var row_label = $("<div />", {'class': "row", 'id': 'label_sin_' + count});
    var row_form = $("<div />", {'class': "row", 'id': 'input_sin_' + count});


    var h4 = $("<h4 />", {'id': "id_nombre_frasco"});

    console.log(count);
    var span_label = $("<span />", {'class': "label"}).text("Sinonimo #" + (parseInt(count) + 1) + ":");

    var input = $('<input />', {
        'id': 'id_sinonimos_'+reactivo_id+'-' + count + '-sinonimo',
        'class': 'form-control',
        'maxlength': "150",
        "type": "text",
        "name": 'sinonimos_'+reactivo_id+'-' + count + '-sinonimo'
    });

    row_form.append($("<div />", {'class': "col-xs-10"}).append(input));
    var row_form_button = row_form.append($("<div />", {'class': "col-xs-2"}).append($("<a />", {
        'class': 'btn btn-danger del_sin_btn_list',
        'data-id': count,
        'data-reactivo': reactivo_id
    }).text(" Eliminar")));

    $('#formset_list_'+reactivo_id+' #forms_sin_list_'+reactivo_id).append(row_label.append(h4.append(span_label)));
    $('#formset_list_'+reactivo_id+' #forms_sin_list_'+reactivo_id).append(row_form_button);
    $('#formset_list_'+reactivo_id+' #id_sinonimos_'+reactivo_id+'-TOTAL_FORMS').val(parseInt(count) + 1);
});

$(document).on("click", ".del_sin_btn_list", function () {
    var reactivo_id = $(this).data('reactivo');
    var count = $('#formset_list_'+reactivo_id+' #forms_sin_list_'+reactivo_id+' >div').length / 2;
    var id = $(this).data('id');

    console.log("Heyyyyyyyyyyyyyyyy " + id);
    $('#formset_list_'+reactivo_id+' #forms_sin_list_'+reactivo_id+' >div').remove('#label_sin_' + id);
    $('#formset_list_'+reactivo_id+' #forms_sin_list_'+reactivo_id+' >div').remove('#input_sin_' + id);

    var i = id + 1;
    while (i < count) {
        $('#formset_list_'+reactivo_id+' #forms_sin_list_'+reactivo_id+' #label_sin_' + i + ' h4 span').text("Sinonimo #" + (i) + ":");
        $('#formset_list_'+reactivo_id+' #forms_sin_list_'+reactivo_id+' #label_sin_' + i).attr("id","label_sin_" + (i-1));
        $('#formset_list_'+reactivo_id+' #forms_sin_list_'+reactivo_id+' #input_sin_' + i).attr("id","input_sin_" + (i-1));
        $('#formset_list_'+reactivo_id+' #forms_sin_list_'+reactivo_id+' #input_sin_' + (i-1) + ' div input').attr({"id":"id_sinonimos_"+reactivo_id+"-" + (i-1) + "-sinonimo", "name": "sinonimos_"+reactivo_id+"-" + (i-1) + "-sinonimo"});
        $('#formset_list_'+reactivo_id+' #forms_sin_list_'+reactivo_id+' #input_sin_' + (i-1) + ' div a').attr("data-id", (i-1));
        console.log("current id "+i);
        i++;
    }

    $('#formset_list_'+reactivo_id+' #id_sinonimos_'+reactivo_id+'-TOTAL_FORMS').val(parseInt(count) - 1);
});