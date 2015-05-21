/*!
 * auhtor: Luis Eduardo Miranda Barja
 * (C) 2015 - mbarjaedu13@gmail.com
 */
$(function(){
	$('.message-menu').addClass('active');
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
			}
			else if(oval==3){
				nro_control.attr('name','nro_control').removeClass('only_g_names').addClass('only_msg_number').prev().text('Semana:').end();
			}
			else if(oval==4){
				nro_control.attr('name','nro_control').removeClass('only_g_names').addClass('only_msg_number').prev().text('Día:').end();
			} else{
				nro_control.attr('name','nro_control').removeClass('only_g_names').addClass('only_msg_number').prev().text('Nro. de Control:').end();
			}
		}
	});
	$('form').on({
		submit:function(e){
			e.preventDefault();
			e.stopPropagation();
			var oform = $(this), btn_submit = oform.find('button[type=submit]');
			btn_submit.disable().hide();
			$.post(
				'/mensajes/adicionar_msj',
				data = oform.form2Dict(),
				function(response){
					if(response){
						location.href='/mensajes/gestion';
					} else{
						prtn.removeClass('has-success').addClass('has-error');
						feedback.removeClass('fa-check').addClass('fa-times');
						btn_submit.enable().show();
					}
				}
			);
		}
	});
});