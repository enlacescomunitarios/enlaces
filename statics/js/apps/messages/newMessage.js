/*!
 * auhtor: Luis Eduardo Miranda Barja
 * (C) 2015 - mbarjaedu13@gmail.com
 */
$(function(){
	$('.message-menu, .sms-catalog').addClass('active');
	$('#back, .back').on({
		click:function(e){
			e.preventDefault();
			location.href='/mensajes/gestion';
		}
	});
	var nro_control = $('input[name=nro_control]'), prtn = nro_control.closest('.form-group'), feedback = $(prtn).find('.form-control-feedback');
	$('#tipo').on({
		change:function(e){
			var oval = +$(this).val();
			nro_control.val('');
			prtn.removeClass('has-success has-error');
			feedback.removeClass('fa-check fa-times');
			if(oval==5){
				nro_control.attr('name','titulo').removeClass('only_msg_number').addClass('only_g_names').prev().text('Título:').end();
			} else{
				nro_control.attr('name','nro_control').removeClass('only_g_names').addClass('only_msg_number').prev().text('Nro. de Control:').end();
			}
		}
	});
	$('.fileinput').fileinput();
	var oaudio = $('input[name=audio]');
	$('form').on({
		submit:function(e){
			e.preventDefault();
			e.stopPropagation();
			var btn_submit = $('button[type=submit]');
			//console.log(oaudio[0].files[0]);
			btn_submit.disable().hide();
			if(oaudio.val().length){
				$.ajax({
					url: '/mensajes/adicionar_msj',
					type: 'POST',
					data:  new FormData(this),
					mimeType:"multipart/form-data",
					contentType: false,
					cache: false,
					processData:false,
					success: function(response){
						if(response){
							location.href='/mensajes/gestion';
						} else{
							prtn.removeClass('has-success').addClass('has-error');
							feedback.removeClass('fa-check').addClass('fa-times');
							btn_submit.enable().show();
						}
					}
				});
			} else {
				btn_submit.enable().show();
			}
		}
	});
});