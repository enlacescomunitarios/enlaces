/*!
 * auhtor: Luis Eduardo Miranda Barja
 * (C) 2015 - mbarjaedu13@gmail.com
 */
$(function(){
	$.post(
		'/etnias/disponibles',
		data = {'_xsrf':getCookie('_xsrf')},
		function(response){
			$('#inputId_etn').html(tmpl_etnias(response));
			$('#inputId_etnc').html($('#inputId_etn').html());
		}
	);
	$.post(
		'/redes_salud/geografia',
		data = {'_xsrf':getCookie('_xsrf')},
		function(response){
			var options = ['<option value="-1">-- Elija Una --</option>'];
			for (var i = 0; i < response.length; i++) {
				var red = response[i];
				options.push('<option value="'+red.id_red+'" data-municipios=\''+JSON.stringify(red.municipios)+'\'>'+red.nombre+'</option>');
			}
			$('#inputRedes').html(options.join(''));
		}
	);
	$('#inputRedes').on({
		change:function(e){
			var o_sel = $(this), o_val = +$(this).val();
			$('#inputMunicipio').html('<option value="-1">-- Elija Uno --</option>').trigger('change');
			$('#inputId_com').html('<option value="-1">-- Elija Una --</option>').trigger('change');
			if(o_val != -1){
				var municipios = o_sel.find('option[value="'+o_val+'"]').data('municipios'), options = ['<option value="-1">-- Elija Uno --</option>'];
				for (var i = 0; i < municipios.length; i++) {
					var mup = municipios[i];
					options.push('<option value="'+mup.id_mup+'" data-comunidades=\''+JSON.stringify(mup.comunidades)+'\'>'+mup.nombre+'</option>');
				}
				$('#inputMunicipio').html(options.join(''));
			}
		}
	});
	$('#inputMunicipio').on({
		change:function(e){
			var o_sel = $(this), o_val = +$(this).val();
			$('#inputId_com').html('<option value="-1">-- Elija Una --</option>').trigger('change');
			if(o_val != -1){
				var comunidades = o_sel.find('option[value="'+o_val+'"]').data('comunidades'), options = ['<option value="-1">-- Elija Una --</option>'];
				for (var i = 0; i < comunidades.length; i++) {
					var com = comunidades[i];
					options.push('<option value="'+com.id_com+'">'+com.nombre+'</option>');
				}
				$('#inputId_com').html(options.join(''));
			}
		}
	});
	var tmpl_etnias = function(olist){
			var options = ['<option value="-1">-- Elija Una --</option>'];
			for (var i = 0; i < olist.length; i++) {
				var obj = olist[i];
				options.push('<option value="'+obj.id_etn+'">'+obj.nombre+'</option>');
			}
			return options.join('');
		},
		check_pregnantphone = function(num){
			var tmp = null;
			$.ajaxSetup({async: false});
			$.post(
				'/personas/v_pregnantstelf',
				data = {'_xsrf':getCookie('_xsrf'),'telf':num},
				function(response){
					tmp = response;
				}
			);
			$.ajaxSetup({async: true});
			return tmp;
		},
		check_contactphone = function(num){
			var tmp = null;
			$.ajaxSetup({async: false});
			$.post(
				'/personas/v_telf',
				data = {'_xsrf':getCookie('_xsrf'),'telf':num},
				function(response){
					tmp = response;
				}
			);
			$.ajaxSetup({async: true});
			return tmp;
		},
		contacForm = $('.contact-form').clone();
	//$('.contact-form').html('');
	//$('#delContact').disable();
	$('#inputTelf').on({
		blur:function(e){
			var preg_telf = $(this), o_val = $(this).val(), chk_ptrn = $(this).data('pattern');
			$('form').find('.prg-name').text('Nueva Embarazada').end().find('.contact-name').text('Contacto');
			$('.contact-form').html('').html(contacForm.html()).find('#inputId_etnc').html($('#inputId_etn').html());
			if(o_val.match(chk_ptrn)==null && o_val.length==0){
				$('.prg_signal').find('select').find('option[value="1"], option[value="2"]').disable().end().find('option[value="0"]').attr('selected',true).end().trigger('change');
				//$('.contact-form').html(contacForm.html());
				//$('#inputId_etnc').html($('#inputId_etn').html());
				$('.contact-form').html('').html(contacForm.html()).find('#inputId_etnc').html($('#inputId_etn').html());
				//$('form').find('#addContact').attr('id','delContact').removeClass('btn-info').addClass('btn-danger');
				//$('form').find('#addContact,#delContact').disable().attr('id','delContact').removeClass('btn-info').addClass('btn-danger');
			} else{
				if(o_val.length==8 && $.type(+o_val)=='number'){
					var cell_flag = check_pregnantphone(o_val);
					//console.log(cell_flag);
					//$('form').find('#addContact,#delContact').enable();
					if(cell_flag.status==false){
						$('.prg_signal').find('select').find('option[value="1"]').attr('selected',true).enable().end().trigger('change');
						preg_telf.closest('.form-group').removeClass("has-error").addClass("has-success");
						//$('.contact-form').html('');
					} else if(cell_flag.status==true){
						preg_telf.closest('.form-group').removeClass("has-error").addClass("has-success");
						//$('.contact-form').html('');
						/*
						$.post(
							'/personas/getbycellphone',
							data = {'_xsrf':getCookie('_xsrf'),'telf':o_val},
							function(response){
								$('form').find('.prg-name').text(response.persona).end().find('.prg_optional').disable().find(':input').disable().end().hide().end();
							}
						);*/
						$('form').find('.prg-name').text(cell_flag.p_data).end().find('.prg_optional').disable().find(':input').disable().end().hide().end();
					} else{
						//alert('El nro. '+o_val+', se encuentra registrado..!');
						//preg_telf.closest('.form-group').removeClass("has-success").addClass("has-error");
						$('.prg_signal').find('select').find('option[value="1"]').removeAttr('selected').disable().end().trigger('change');
						preg_telf.val('').focus();
						swal({
							title:'Error!',
							text: cell_flag.p_data!=null?(cell_flag.p_data+'.\nEstá registrado con el nro. '+o_val):'',
							type:'error',
							confirmButtonText: "Continuar",
							closeOnConfirm: false
						});
					}
				} else{
					preg_telf.closest('.form-group').removeClass("has-success").addClass("has-error");
				}
			}
		}
	});
	$('input[name=ci]').on({
		blur:function(e){
			var o_ci = $(this), o_val = o_ci.val();
			if(o_val.length>6 && o_val.length<9){
				$.post(
					'/personas/v_ci',
					data = {'_xsrf':getCookie('_xsrf'),'ci':o_val},
					function(response){
						if(response){
							o_ci.val('').focus().closest('.form-group').removeClass("has-success").addClass("has-error");
							swal({
								title: 'Error!',
								text: '"'+o_val+'", se encuentra registrado!.\nPor favor elija otro.',
								type: 'error',
								confirmButtonText: "Continuar",
								closeOnConfirm: false
							});
						} else{
							o_ci.closest('.form-group').removeClass("has-error").addClass("has-success");
						}
					}
				);
			} else{
				o_ci.val('').closest('.form-group').removeClass("has-success has-error");
			}
		}
	});
	/*
	$('form').on('click', '#addContact', function(e){
		e.preventDefault();
		$('.contact-form').html(contacForm.html()).find('#inputId_etnc').html($('#inputId_etn').html());
		$(this).attr('id','delContact').removeClass('btn-info').addClass('btn-danger');
	});
	$('form').on('click', '#delContact', function(e){
		e.preventDefault();
		$('form').find('.contact-name').text('Contacto');
		$('.contact-form').html('');
		$(this).attr('id','addContact').removeClass('btn-danger').addClass('btn-info');
	});
	*/
	$('form').on('blur', '#inputTelfc', function(e){
		var o_val = $(this).val(), chk_ptrn = $(this).data('pattern'), o_ctelf = $(this), prg_cell = $('#inputTelf').val();
		if(o_val.match(chk_ptrn)!=null && o_val!=prg_cell){
			if(check_contactphone(o_val)==false){
				$('form').find('.contact-name').text('Contacto').end().find('.optional').enable().show();
				o_ctelf.closest('.form-group').removeClass("has-error").addClass("has-success");
				$('#inputCoberturac').find('option[value="1"]').attr('selected',true).end().trigger('change');
			} else{
				//o_ctelf.closest('.form-group').removeClass("has-success").addClass("has-error");
				//alert('El nro. '+o_val+', se encuentra registrado..!');
				//o_ctelf.val('').focus();
				$.post(
					'/personas/getbycellphone',
					data = {'_xsrf':getCookie('_xsrf'),'telf':o_val},
					function(response){
						$('form').find('.optional').disable().find(':input').disable().end().hide().end().find('.contact-name').text(response.persona);
					}
				);
			}
		} else{
			//o_ctelf.focus();
			o_ctelf.val('').closest('.form-group').removeClass("has-success").addClass("has-error").find('span').removeClass('fa-check').addClass('fa-times');
			$('form').find('.optional').enable().find(':input').enable().end().show().end().find('.contact-name').text('Contacto');
		}
	});
	$('form').on('change', 'select', function(e){
		var o_sel = $(this);
		if(o_sel.val()!='-1'){
			o_sel.closest('.form-group').removeClass("has-error").addClass("has-success");
		} else{
			o_sel.closest('.form-group').removeClass("has-success").addClass("has-error");
		}
	});
	$('form').on({
		submit:function(e){
			e.preventDefault();
			e.stopPropagation();
			var oform = $(this), btn_submit = oform.find('button[type=submit]');
			btn_submit.disable().hide();
			$.post(
				'/embarazadas/nueva_embarazada',
				data = oform.form2Dict(),
				function(response){
					//console.log('logging:',response);
					if(response){
						location.href='/embarazadas/gestion';
					} else{
						btn_submit.enable().show();
						$('#inputParto_prob').val('').focus().closest('.form-group').removeClass('has-success').addClass('has-error').find('span').removeClass('fa-check').addClass('fa-times');
					}
				}
			);
		}
	});
});