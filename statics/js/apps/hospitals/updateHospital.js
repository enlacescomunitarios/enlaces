/*!
 * auhtor: Luis Eduardo Miranda Barja
 * (C) 2015 - mbarjaedu13@gmail.com
 */
$(function(){
	$('.manager-menu, .health-sub').addClass('active');
	var o_comunities = $('.key').data('key'), o_key = $('.breadcrumb').data('key'),
		centros = ['Puesto de Salud','Centro de Salud','1er. Nivel','2do. Nivel','3er. Nivel'],
		options = [], o_prestaciones = JSON.stringify($('.key').data('prest')),
		tmpl = function(obj){
			return ''+
			'<div class="input-group">'+
				'<span class="input-group-addon">'+
					'<input type="checkbox" name="id_com" value="'+obj.id+'">'+
				'</span>'+
				'<label class="form-control input-sm">'+obj.nombre+'</label>'+
			'</div>';
		},
		prest = function(obj){
			return ''+
			'<div class="input-group">'+
				'<span class="input-group-addon">'+
					'<input type="checkbox" name="id_pst" value="'+obj.id_pst+'">'+
				'</span>'+
				'<label class="form-control input-sm">'+obj.nombre+'</label>'+
			'</div>';
		};
	//console.log('o_key',o_key);
	for (var i = 0; i < centros.length; i++) {
		if(centros[i]==o_key.tipo){
			options.push('<option value="'+centros[i]+'" selected>'+centros[i]+'</option>');
		} else{
			options.push('<option value="'+centros[i]+'">'+centros[i]+'</option>');
		}
	};
	$('#inputTipo').html(options.join(''));
	for (var i = 0; i < o_comunities.length; i++) {
		if(o_key.com!=o_comunities[i].id){
			$('#comunidades').append(tmpl(o_comunities[i]));
		}
	};
	$.post(
		'/prestaciones/disponibles',
		data = {'_xsrf':getCookie('_xsrf'), 'prestaciones': o_prestaciones},
		function(response){
			if($.type(response)=='array'){
				for (var i = 0; i < response.length; i++) {
					$('#prestaciones').append(prest(response[i]));
				};
			}
		}
	);
	$('.networks').on({
		click:function(e){
			e.preventDefault();
			location.href='/redes_salud/gestion';
		}
	});
	$('.net').on({
		click:function(e){
			e.preventDefault();
			location.href='/municipios/gestion?id_red='+o_key.red;
		}
	});
	$('.mup').on({
		click:function(e){
			e.preventDefault();
			location.href='/comunidades/gestion?id_mup='+o_key.mup
		}
	});
	$('.back').on({
		click:function(e){
			e.preventDefault();
			location.href='/centros_salud/gestion?id_com='+o_key.com;
		}
	});
});