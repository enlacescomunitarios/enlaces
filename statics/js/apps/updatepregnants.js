$(function(){
	var checkfields = $('form').data('key'),
		ldetnias = function(etnias){
			var options = [$('<option value="-1">-- Elija Una --</option>')];
			for (var i = 0; i < etnias.length; i++) {
				var etn = etnias[i], opt_etn = $('<option/>', {'value':etn.id_etn, 'text':etn.nombre});
				if(etn.id_etn==checkfields.id_etn){
					opt_etn.attr('selected',true);
				}
				options.push(opt_etn);
			}
			return options;
		},
		ldRedes = function(redes){
			var options = [$('<option value="-1">-- Elija Una --</option>')];
			for (var i = 0; i < redes.length; i++) {
				var red = redes[i], opt_red = $('<option/>', {'value':red.id_red, 'text':red.nombre}).data('municipios', red.municipios);
				if(checkfields.id_red==red.id_red){
					opt_red.attr('selected',true);
				}
				options.push(opt_red);
			}
			return options;
		},
		ldMunicipios = function(municipios){
			var options = [$('<option value="-1">-- Elija Uno --</option>')];
			for (var i = 0; i < municipios.length; i++) {
				var mup = municipios[i], opt_mup = $('<option/>', {'value':mup.id_mup, 'text':mup.nombre}).data('comunidades', mup.comunidades);
				if(checkfields.id_mup==mup.id_mup){
					opt_mup.attr('selected',true);
				}
				options.push(opt_mup);
			}
			return options;
		},
		ldComunidades = function(comunidades){
			var options = [$('<option value="-1">-- Elija Uno --</option>')];
			for (var i = 0; i < comunidades.length; i++) {
				var com = comunidades[i], opt_com = $('<option/>', {'value':com.id_com, 'text':com.nombre});
				if(checkfields.id_com==com.id_com){
					opt_com.attr('selected',true);
				}
				options.push(opt_com);
			}
			return options;
		};
	if(checkfields.is_pregnant){
		$.post(
			'/etnias/disponibles',
			data = {'_xsrf':getCookie('_xsrf')},
			function(response){
				$('#etnia').html(ldetnias(response));
			}
		);
		$.post(
			'/redes_salud/geografia',
			data = {'_xsrf':$('input[name=_xsrf]').val()},
			function(response){
				$('#red').html(ldRedes(response)).on({
					change:function(){
						var o_val = +$(this).val(), municipios = $(this).find('option[value="'+o_val+'"]').data('municipios');
						if(o_val>0){
							$('#municipio').html(ldMunicipios(municipios)).on({
								change:function(){
									var o_val = +$(this).val();
									if(o_val>0){
										comunidades = $(this).find('option[value="'+o_val+'"]').data('comunidades');
										$('#comunidad').html(ldComunidades(comunidades));
									} else{
										$('#comunidad').html('<option value="-1">-- Elija Una --</option>');
									}
								}
							}).change();
						} else{
							$('#municipio').html('<option value="-1">-- Elija Uno --</option>');
							$('#comunidad').html('<option value="-1">-- Elija Una --</option>');
						}
					}
				}).change();
			}
		);
	} else{
		$('.locations').disable().hide();
	}
	var pregnant_telf = +$('input[name=telf]').val(), contact_telf = $('input[name=c_telf]').val(), current_ci = $('input[name=ci]').val();
	$('input[name=telf]').on({
		blur:function(e){
			var o_telf = $(this), o_val = $(this).val();
			if(pregnant_telf != +o_val && o_val.length==8){
				if(o_val != contact_telf){
					$.post(
						'/personas/v_telf',
						data = {'_xsrf':$('input[name=_xsrf]').val(), 'telf':o_val},
						function(response){
							//console.log(response);
							if(response){
								o_telf.val(pregnant_telf).focus().closest('.form-group').removeClass('has-success has-error');
								swal({
									title: 'Error!',
									text: 'El nro. '+o_val+', está registrado!.\nPor favor use otro.',
									type: 'error',
									confirmButtonText: 'Continuar',
									closeOnConfirm: false
								});
							}
						}
					);
				} else{
					o_telf.val(pregnant_telf).focus().closest('.form-group').removeClass('has-success has-error');
				}
			}
		}
	});
	$('input[name=c_telf]').on({
		blur:function(e){
			var o_telf = $(this), o_val = o_telf.val();
			if(o_val.length==8 && o_val!=contact_telf){
				if(o_val!=pregnant_telf){
					$.post(
						'/personas/v_telf',
						data = {'_xsrf':$('input[name=_xsrf]').val(), 'telf':o_val},
						function(response){
							//console.log(response);
							if(response){
								$('form').find('.optional').show().end().find('.contact-name').text('Contacto');
								//o_telf.val(contact_telf).focus().closest('.form-group').removeClass('has-success has-error');
								$.post(
									'/personas/getbycellphone',
									data = {'_xsrf':getCookie('_xsrf'),'telf':o_val},
									function(response){
										if(response){
											$('form').find('.optional').hide().end().find('.contact-name').text(response.persona);
										}
									}
								);
							}
						}
					);
				} else{
					$('form').find('.optional').show().end().find('.contact-name').text('Contacto');
					o_telf.val(contact_telf).focus().closest('.form-group').removeClass('has-success has-error').find('span').removeClass('fa-check fa-time');
				}
			} else{
				$('form').find('.optional').show().end().find('.contact-name').text('Contacto');
				o_telf.val(contact_telf).closest('.form-group').removeClass('has-success has-error').find('span').removeClass('fa-check fa-time');
			}
		}
	});
	current_ci = current_ci.length==8?current_ci:'';
	$('input[name=ci]').on({
		blur:function(e){
			var o_ci = $(this), ci_val = $(this).val();
			if(ci_val.length>=7 && ci_val.length<=8 && ci_val!=current_ci){
				$.post(
					'/personas/v_ci',
					data = {'_xsrf':getCookie('_xsrf'),'ci':o_ci.val()},
					function(response){
						if(response){
							o_ci.val(current_ci).focus().closest('.form-group').removeClass("has-success has-error");
							swal({
								title: 'Error!',
								text: 'El CI: '+ci_val+', está registrado!.\nPor favor use otro.',
								type: 'error',
								confirmButtonText: 'Continuar',
								closeOnConfirm: false
							});
						} else{
							o_ci.closest('.form-group').removeClass("has-error").addClass("has-success").find('span').removeClass('fa-times').addClass('fa fa-check');
						}
					}
				);
			}
		}
	});
	$('form').on({
		submit:function(e){
			e.preventDefault();
			e.stopPropagation();
			var oform = $(this), btn_submit = $(this).find('button[type=submit]');
			btn_submit.disable().hide();
			$.post(
				'/embarazadas/modificar_embarazada',
				data = oform.form2Dict(),
				function(response){
					if(response){
						location.href='/embarazos/gestion?id_per='+$('input[name=id_per]').val();
					} else{
						btn_submit.enable().show();
					}
				}
			);
		}
	});
});