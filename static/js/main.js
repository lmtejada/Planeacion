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
                if(this.value == ''){
                    enviar = false;
                    $('#errors_'+politica_id).html("<p>Para guardar el formulario debe diligenciar todos los campos.</p>"); 
                    $('#errors_'+politica_id).show();
                    return;
                }
            }
        });
    } 

    if(enviar){
        var csrftoken = getCookie('csrftoken');
        $('input[name=csrfmiddlewaretoken]').val(csrftoken);
        $(form).submit();
    }
});

$('#enviar').on('click', function(event){	
    event.preventDefault();
    var form = $(this).parents('.formulario');
    var id = $(form).attr('id');
   
    $('#'+id).append("<input type='hidden' name='enviado' value='true'/>");
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
        data : {indicador : indicador_id},

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
    $("#data_"+politica_id).html("<h3>Plan de desarrollo</h3><hr/>"+
                                 "<div class='row'><div class='col-md-6'><label>Eje estratégico</label><p>"+obj['data']['eje_estrategico']+"</p></div>"+
                                 "<div class='col-md-6'><label>Programa</label><p>"+obj['data']['programa']+"</p></div></div>"+
                                 "<div class='row'><div class='col-md-6'><label>Subprograma</label><p>"+obj['data']['subprograma']+"</p></div>"+
                                 "<div class='col-md-6'><label>Proyecto</label><p>"+obj['data']['proyecto']+"</p></div></div>"+
                                 "<hr/><h3>Información de la política</h3><hr/>"+
                                 "<div class='row'><div class='col-md-6'><label>"+obj['data']['nivel1'].nombre+"</label><p>"+obj['data']['nivel1'].valor+"</p></div>"+
                                 "<div class='col-md-6'><label>"+obj['data']['nivel2'].nombre+"</label><p>"+obj['data']['nivel2'].valor+"</p></div></div>"+
                                 "<div class='row'><div class='col-md-6'><label>"+obj['data']['nivel3'].nombre+"</label><p>"+obj['data']['nivel3'].valor+"</p></div></div>");
    $("#data_"+politica_id).show();
    $("#wrapper_"+politica_id).show();

    var respuestas = obj['respuestas'];
    if(jQuery.isEmptyObject(respuestas)){
        $(':input:not([type=button], [name=form_id])', '#'+id).each(function() {
        if(!$(this).is('select'))
            $(this).val('');
        });
    } else {
        console.log(obj['data']['accion']);
        $("#accion_"+politica_id).val(obj['data']['accion']);
        $("#ubicacion_"+politica_id).val(obj['data']['ubicacion']);
        $("#soporte_"+politica_id).val(obj['data']['soporte']);
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
