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
    } else {
        $(':input:not([type=button])', '#'+id).each(function() {
            if(!$(this).is(':hidden')){
                if(this.value == '' || this.value == 'null'){
                    enviar = false;
                    $('#errors_'+politica_id).html("<p>Para guardar el formulario debe diligenciar todos los campos.</p>"); 
                    $('#errors_'+politica_id).show();
                    return;
                }
            }
        });
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
    //$('#'+id).append("<input type='hidden' name='activo' value='false'/>");

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
});

$('#calificacion').on('change', function(event){
    $("#mensajes").html(''); 
    var value = $(this).val();
    if(value == 'no_aprobado'){
        $("#observaciones").html('<label for="observaciones">Observaciones</label><textarea rows="4" class="form-control" name="observaciones"></textarea>');
    } else {
        $("#observaciones").html('');
    }
});

$('#calificar').on('click', function(event){   
    event.preventDefault();
    var form = $(this).parents('.formulario');
    var csrftoken = getCookie('csrftoken');
    if($("#calificacion").val() != 'null'){
        $('input[name=csrfmiddlewaretoken]').val(csrftoken);
        $(form).submit();
    } else {
        $("#mensajes").html('<div class="alert alert-danger text-center messages" style="opacity: 0.7">Debe seleccionar una calificación</div>');
    }
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

function llenarFormulario(json, politica_id){
	var obj = JSON.parse(json);
    var id = "formulario_"+politica_id;
    console.log(obj);
    $("#data_"+politica_id).html("<h3>Información de la política</h3><hr/>"+
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
        for(var key in respuestas) {
            $("#respuesta_"+politica_id+"_"+respuestas[key].pregunta_id).val(respuestas[key].respuesta_id);
            $("#valor_"+politica_id+"_"+respuestas[key].pregunta_id).val(respuestas[key].valor);
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

    if($("#"+id).hasClass('detalle')){
        $(':input:not([name=indicador])', '#'+id).each(function() {
            $(this).prop('disabled', true); 
        });
    }
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
    console.log("id usuario: " + id);
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