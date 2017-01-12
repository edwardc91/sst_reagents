// configuraciones para los eventos adversos
var nombre_panel_group = "#accordion"; // id
var nombre_boton_eliminar = ".deleteReactivo"; // Clase
var nombre_formulario_modal = "#form_del_reactivo"; //id
var nombre_ventana_modal = "#delReactivoModal"; // id

// datos del reactivo
var nombre_form_act_datos = ".form_datos_reactivo";
var nombre_info_modal = "#infoReactivoModal";

// existencias del reactivo
var nombre_form_existencias = ".form_existencias";

$(document).on('ready', function () {
    console.log("document ready");
    $(nombre_boton_eliminar).on('click', function (e) {
        e.preventDefault();
        var name = $(this).data('name');
        var id = $(this).data('id');
        $('#modal_reactivo_nombre').val(id);
        $('#modal_name_reactivo').text(name);
    });


    var options_del_reactivo = {
        success: function (response) {
            console.log("success");
            if (response.status == "True") {
                var reactivo_id = response.reactivo_id;
                var elementos = $(nombre_panel_group + ' >div').length;
                if (elementos == 1) {
                    location.reload();
                } else {
                    $('#panel_' + reactivo_id).remove();
                    //alert("FUNCIONA");
                    $(nombre_ventana_modal).modal('hide');
                    console.log("borrado");
                }

            } else {
                alert("Hubo un error al eliminar!");
                $(nombre_ventana_modal).modal('hide');
            }
        }
    };

    var options_act_reactivo = {
        success: function (response) {
            if (response.status == "True") {
                location.reload(true);
            } else {
                $('#modalInfoTitleLabel').attr("class", "modal-title text-danger");
                $('#modalInfoTitleLabel').text("Error en los datos del reactivo");
                $('#textBodyInfoModal').text("");
                $('#buttonAceptarInfoModal').attr("class", "btn btn-danger");
                var error_list = response.error_list;
                for(var i = 0; i < error_list.length; i++){
                    $('#textBodyInfoModal').append($('<span />',{'text': error_list[i]}));
                    $('#textBodyInfoModal').append($('<br />'));
                }
                $(nombre_info_modal).modal('show');
            }

        }
    };

    var options_act_existencias = {
        success: function (response) {
            if (response.status == "True") {
                location.reload(true);
            } else {
                $('#modalInfoTitleLabel').attr("class", "modal-title text-danger");
                $('#modalInfoTitleLabel').text("Error en los datos de la existencia(s)");
                $('#textBodyInfoModal').text("");
                $('#buttonAceptarInfoModal').attr("class", "btn btn-danger");
                var error_list = response.error_list;
                for(var i = 0; i < error_list.length; i++){
                    $('#textBodyInfoModal').append($('<span />',{'text': error_list[i]}));
                    $('#textBodyInfoModal').append($('<br />'));
                }
                $(nombre_info_modal).modal('show');
            }

        }
    };


    $(nombre_formulario_modal).ajaxForm(options_del_reactivo);
    $(nombre_form_act_datos).ajaxForm(options_act_reactivo);
    $(nombre_form_existencias).ajaxForm(options_act_existencias);
});