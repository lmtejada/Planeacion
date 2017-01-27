$(document).ready(function(){
    $(".chosen").chosen();
});

$(document).click(function() {
    //$(".messages").remove();
});

$('.nav').click(function() {
    $(".messages").remove();
    //$('.errors').html('');
    //$('.errors').hide();
});

$('input').on('change', function() {
    //$('.errors').html('');
    //$('.errors').hide();
});

$('select').on('change', function() {
    //$('.errors').html('');
    //$('.errors').hide();
});

$('.guardar').on('click', function(event){	
    event.preventDefault();
    var enviar = true;
    var form = $(this).parents('.formulario');
    var id = $(form).attr('id');
    var politica_id = id.split('_');
    politica_id = politica_id[1];

    if($("#indicador_"+politica_id).val() == "null"){
        enviar = false;
        $('#errors_'+politica_id).html("<p>Por favor seleccione un indicador.</p>"); 
        $('#errors_'+politica_id).show();
        window.scrollTo(0,0);
    } else {
        if($("#subprograma_"+politica_id).val() == "null"){
            enviar = false;
            $('#errors_'+politica_id).html("<p>Por favor seleccione un subprograma.</p>"); 
            $('#errors_'+politica_id).show();
            window.scrollTo(0,0);
        } else {
            var total1 = parseFloat($("#valor_"+politica_id+"_15").val()) + parseFloat($("#valor_"+politica_id+"_16").val());
            if(isNaN(total1))
                total1 = 0;

            var total2 = parseFloat($("#valor_"+politica_id+"_17").val()) + parseFloat($("#valor_"+politica_id+"_18").val());
            if(isNaN(total2))
                total2 = 0;

            if(total1 != 0 && total2 != 0 && total1 != total2){
                enviar = false;
                $('#errors_'+politica_id).html("<p>El total de la población atendida debe ser igual para el género y la zona.</p>"); 
                $('#errors_'+politica_id).show();
                window.scrollTo(0,0);
            } else {
                $(':input:not([type=button])', '#'+id).each(function() {
                    if(!$(this).is(':hidden')){
                        if(typeof $(this).attr('name') != 'undefined'){
                            if(this.value == ''){
                                enviar = false;
                                $('#errors_'+politica_id).html("<p>Para guardar el formulario debe diligenciar todos los campos.</p>"); 
                                $('#errors_'+politica_id).show();
                                window.scrollTo(0,0);
                                return;
                            }
                        }
                    } else if ($(this).hasClass( "chosen" )){   
                        if(this.value == 'null'){
                            enviar = false;
                            $('#errors_'+politica_id).html("<p>Para guardar el formulario debe diligenciar todos los campos.</p>"); 
                            $('#errors_'+politica_id).show();
                            window.scrollTo(0,0);
                            return;
                        }
                    }
                });
            }
        }
    } 

    if(enviar){
        $('#'+id).append("<input type='hidden' name='politica' value='"+politica_id+"'/>");
        var csrftoken = getCookie('csrftoken');
        $('input[name=csrfmiddlewaretoken]').val(csrftoken);
        $(form).submit();
    }
});

$('.enviar').on('click', function(event){	
    event.preventDefault();
    var form = $(this).parents('.formulario');
    var id = $(form).attr('id');
    var tmp = id.split('_');
    tmp = tmp[2]

    $('#'+id).append("<input type='hidden' name='enviado' value='true'/>");
    $('#'+id).append("<input type='hidden' name='politica' value='"+tmp+"'/>");

    var csrftoken = getCookie('csrftoken');
    $('input[name=csrfmiddlewaretoken]').val(csrftoken);
    $(form).submit();
});

$('.indicadores').on('change', function(event){	
    var value = $(this).val();
    var id = $(this).attr('id');
    id = id.split('_');
    id = id[1];
    $("#data_"+id).html('');
    $("#data_"+id).hide();
    $("#wrapper_"+id).hide();
    if(value != 'null'){
        $('#errors_'+id).html('');
        $('#errors_'+id).hide();
	    cargarData(value, id);
    } else {
    	var form = "formulario_"+id;
        $(':input:not([name=indicador])', '#'+form).each(function() {
            $(this).prop('disabled', false);
        });
	    $(':input:not([type=button])', '#'+form).each(function() {
			if(!$(this).is('select'))
                $(this).val('');
            else
                $(this).val('null');
		});
    }

    $(".chosen").trigger("chosen:updated");

});

$('.indicador_respuesta').on('change', function(event){ 
    var value = $(this).val();
    var id = $(this).attr('id');
    id = id.split('_');
    id = id[1];
    $("#data_"+id).html('');
    $("#data_"+id).hide();
    $("#wrapper_"+id).hide();
    if(value != 'null'){
        $('#errors_'+id).html('');
        $('#errors_'+id).hide();
        cargarDataRespuesta(value, id, $(this).attr('rel'));
    } else {
        var form = "formulario_"+id;
        $(':input:not([name=indicador])', '#'+form).each(function() {
            $(this).prop('disabled', false);
        });
        $(':input:not([type=button])', '#'+form).each(function() {
            if(!$(this).is('select'))
                $(this).val('');
            else
                $(this).val('null');
        });
        $("#observaciones").val('');
    }

    $(".chosen").trigger("chosen:updated");
    
});

$('.subprograma').on('change', function(event){ 
    $(".chosen").trigger("chosen:updated");
});

$('#calificacion').on('change', function(event){
    $("#mensajes").html(''); 
});

$('#calificar').on('click', function(event){   
    event.preventDefault();
    var form = $(this).parents('.formulario');
    var csrftoken = getCookie('csrftoken');
    if($("#calificacion").val() != 'null'){
        $('input[name=csrfmiddlewaretoken]').val(csrftoken);
        $(form).submit();
    } else {
        $("#mensajes").html('<div class="alert alert-danger text-center messages">Debe seleccionar una calificación</div>');
    }
});

$('.observaciones').on('click', function(event){   
    event.preventDefault();
    var enviar = true;
    var form = $(this).parents('form');
    var id = $(this).attr('id');
    var tmp = id.split('_');
    tmp = tmp[1]
    var valor = $("#indicador_"+tmp).val();

    if($("#observaciones").val() == ''){
        $("#mensajes").html('<div class="alert alert-danger text-center messages">Debe ingresar una observación</div>');
        window.scrollTo(0,0);
        enviar = false;
    }

    if(valor == 'null'){
        $("#mensajes").html('<div class="alert alert-danger text-center messages">Debe seleccionar un indicador</div>');
        window.scrollTo(0,0);
        enviar = false;
    }

    if(enviar){
        $(form).append("<input type='hidden' name='indicador' value='"+valor+"'/>");
        var csrftoken = getCookie('csrftoken');
        $('input[name=csrfmiddlewaretoken]').val(csrftoken);
        $(form).submit();
    }
});

$('.recurso').on('change', function(event){
    if($(this).val() < 0)
        $(this).val(0);
    var id = $(this).attr('id');
    id = id.split('_');
    id = id[1];   
    var total = parseFloat($("#valor_"+id+"_9").val()) + parseFloat($("#valor_"+id+"_10").val()) + parseFloat($("#valor_"+id+"_11").val()) + parseFloat($("#valor_"+id+"_12").val()) + parseFloat($("#valor_"+id+"_13").val()) + parseFloat($("#valor_"+id+"_14").val());
    if(isNaN(total))
        total = 0;
    $("#total_recursos_"+id).val(total);
});

$('.poblacion').on('change', function(event){
    if($(this).val() < 0)
        $(this).val(0);
    var id = $(this).attr('id');
    id = id.split('_');
    id = id[1];   
    var total = parseFloat($("#valor_"+id+"_15").val()) + parseFloat($("#valor_"+id+"_16").val());
    if(isNaN(total))
        total = 0;

    $("#total_poblacion_"+id).val(total);
});

function cargarData(indicador_id, formulario_id) { 
    $.ajax({
        url : "/seguimiento/get_data/", 
        type : "POST", 
        data : {indicador : indicador_id, politica : formulario_id},

        success : function(json) {
            llenarFormulario(json, formulario_id); 
        },

        error : function(xhr,errmsg,err) {
            $('#errors_'+formulario_id).html("<p>Error al cargar los datos. Por favor actualice la página e intente nuevamente.</p>"); 
            console.log(xhr.status + ": " + xhr.responseText); 
        }
    });
};

function cargarDataRespuesta(indicador_id, politica_id, formulario_id) { 
    $.ajax({
        url : "/consultas/get_data/", 
        type : "POST", 
        data : {indicador : indicador_id, formulario : formulario_id},

        success : function(json) {
            llenarFormulario(json, politica_id); 
        },

        error : function(xhr,errmsg,err) {
            $('#errors_'+formulario_id).html("<p>Error al cargar los datos. Por favor actualice la página e intente nuevamente.</p>"); 
            console.log(xhr.status + ": " + xhr.responseText); 
        }
    });
};

function llenarFormulario(json, politica_id){
	var obj = JSON.parse(json);
    var id = "formulario_"+politica_id;
    $("#data_"+politica_id).html("<hr/><h3>Información de la política</h3><hr/>"+
                                 "<div class='row'><div class='col-md-12'><label>"+obj['data']['nivel1'].nombre+"</label><p>"+obj['data']['nivel1'].valor+"</p></div></div>"+
                                 "<div class='row'><div class='col-md-12'><label>"+obj['data']['nivel2'].nombre+"</label><p>"+obj['data']['nivel2'].valor+"</p></div></div>"+
                                 "<div class='row'><div class='col-md-12'><label>"+obj['data']['nivel3'].nombre+"</label><p>"+obj['data']['nivel3'].valor+"</p></div></div>"+
                                 "<div class='row'><div class='col-md-12'><label>Acción</label><p>"+obj['data']['accion']+"</p></div></div>"+
                                 "<div class='row'><div class='col-md-12'><label>Meta de la política</label><p>"+obj['data']['meta']+"</p></div></div>");
    $("#data_"+politica_id).show();
    $("#wrapper_"+politica_id).show();

    var respuestas = obj['respuestas'];
    if(jQuery.isEmptyObject(respuestas)){
        $(':input:not([type=button], [name=form_id], [name=indicador])', '#'+id).each(function() {
        if(!$(this).is('select'))
            $(this).val('');
        else
            $(this).val('null');
        });
    } else {
        for(var key in respuestas){
            if(key != 'subprograma'){
                $("#respuesta_"+politica_id+"_"+respuestas[key].pregunta_id).val(respuestas[key].respuesta_id);
                $("#valor_"+politica_id+"_"+respuestas[key].pregunta_id).val(respuestas[key].valor);
            } else {
                $("#subprograma_"+politica_id).val(respuestas[key]);
            }
        }
    }

    if(obj['activo']){
        $(':input:not([name=indicador])', '#'+id).each(function() {
            $(this).prop('disabled', false);
        });
    } else {
        if(obj['estado']=='aprobado'){
            $('#errors_'+politica_id).html("<p>El formulario ya fue aprobado y no puede ser modificado.</p>"); 
            $('#errors_'+politica_id).show(); 
        } 
        if(obj['estado']=='pendiente'){
            $('#errors_'+politica_id).html("<p>El formulario se encuentra en proceso de revisión y no puede ser modificado.</p>"); 
            $('#errors_'+politica_id).show(); 
        }
        $(':input:not([name=indicador])', '#'+id).each(function() {
            $(this).prop('disabled', true); 
        });
    }

    if(obj['observaciones']){
        $("#observaciones").val(obj['observaciones']);
    } else {
         $("#observaciones").val('');
    }

    if($("#"+id).hasClass('detalle')){
        $(':input:not([name=indicador])', '#'+id).each(function() {
            $(this).prop('disabled', true); 
        });
    }

    var total = parseFloat($("#valor_"+politica_id+"_15").val()) + parseFloat($("#valor_"+politica_id+"_16").val());
    if(isNaN(total))
        total = 0;
    $("#total_poblacion_"+politica_id).val(total);
    $("#total_poblacion_"+politica_id).prop('disabled', true); 

    var total = parseFloat($("#valor_"+politica_id+"_9").val()) + parseFloat($("#valor_"+politica_id+"_10").val()) + parseFloat($("#valor_"+politica_id+"_11").val()) + parseFloat($("#valor_"+politica_id+"_12").val()) + parseFloat($("#valor_"+politica_id+"_13").val()) + parseFloat($("#valor_"+politica_id+"_14").val());
    if(isNaN(total))
        total = 0;
    $("#total_recursos_"+politica_id).val(total);
    $("#total_recursos_"+politica_id).prop('disabled', true); 
    $(".chosen").trigger("chosen:updated");
};

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$('.eliminar').on('click', function(event){   
    var id = $(this).attr('rel');
    eliminarUsuario(id)
});

function eliminarUsuario(idUsuario) { 
    $.ajax({
        url : "/cuenta/eliminar/", 
        type : "POST", 
        data : {idUsuario : idUsuario},

        success : function(json) {
            mostrarMensaje(json, "success"); 
        },

        error : function(xhr,errmsg,err) {
            mostrarMensaje(xhr.responseText, "error") 
            console.log(xhr.status + ": " + xhr.responseText); 
        }
    });
};

function mostrarMensaje(json, status){
    var obj = JSON.parse(json);
    window.location.hash = 'reload';
    window.location.reload();
}

document.addEventListener("DOMContentLoaded", function(event){
    if(window.location.hash == '#reload'){
        $("#responses").html('<div class="alert alert-success text-center messages" style="opacity: 0.7">El usuario se ha eliminado con éxito</div>');
        window.location.hash = '';
    }
});

