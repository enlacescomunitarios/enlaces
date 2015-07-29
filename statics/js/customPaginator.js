/*!
 * auhtor: Luis Eduardo Miranda Barja
 * (C) 2014 - mbarjaedu13@gmail.com
 */
 $(function(){
 	$('table').find('tbody').find('a, .link').each(function(){
 		var olink = $(this);
 		olink.data('link', olink.attr('href')).removeAttr('href').on({
 			click:function(e){
 				e.preventDefault();
 				location.href = $(this).data('link');
 			}
 		});
 	});
 	$.fn.customPaginator = function(config){
 		//console.log(arguments.length);
 		var optRange = function(range){
	 			var options = [[],[]];
	 			if(arguments.length){
	 				for (var i = 0; i < range.length; i++) {
	 					options[0].push(range[i]); options[1].push(range[i]);
	 				}
	 				options[0].push(10); options[1].push(10);
	 				for(var i=25; i<=100; i=i+25){
	 					options[0].push(i); options[1].push(i);
	 				}
	 			} else{
	 				options[0].push(10); options[1].push(10);
	 				for(var i=25; i<=100; i=i+25){
	 					options[0].push(i); options[1].push(i);
	 				}
	 			}
	 			options[0].push(-1); options[1].push('Todo');
	 			return options;
	 		},
	 		cfg = $.extend({'height': 'auto', sort: true}, config),
	 		$cfg = {
 				//scrollY: 300,
	 			scrollX: true,
	 			//sScrollY: (arguments.length && 'height' in config)?config.height:278,
	 			//sScrollX: 599,
	 			sScrollY: cfg.height,
	 			/*pagingType:'simple_numbers',//'full_numbers'*/
	 			pagingType: 'full_numbers',
	 			sort: cfg.sort,
	 			//lengthMenu: arguments.length==0?optRange():optRange(start,stop,step),
	 			lengthMenu: ('range' in cfg && cfg.range.length)?optRange(cfg.range):optRange(),
	 			language:{
	 				//"lengthMenu": "<span>Mostrar </span>_MENU_<span> datos</span>",
	 				"lengthMenu": "Mostrar _MENU_<span class='itotal'></span>",
	 				"zeroRecords": "Sin datos disponibles!",
	 				"info": "Página _PAGE_ de _PAGES_<i class='ttotal hidden'>_TOTAL_</i>",
	 				"infoEmpty": "Sin datos",
	 				//"infoFiltered": "(filtrado de _MAX_ total entradas)",
	 				"infoFiltered": "",
	 				"search": "",
	 				"paginate": {
	 					"first": " ",//primero
	 					"previous": " ",//anterior
	 					"next": " ",//siguiente
	 					"last": " "//ultimo
	 				}
	 			}
 			};
 		/*
		var myfilter = $('<select class="form-control input-sm myfilter"/>'), list_options = ['<option value="-1">Todos</option>'];
		for(var i=0; i<4; i++){
			var op = $('<option value="'+i+'">Opción '+i+'</option>');
			list_options.push(op);
		}
		myfilter.on({
			change:function(e){
				console.log('ok!');
			}
		}).html(list_options);
		*/
		return this.each(function(){
			var custom_dt = $(this).dataTable($cfg).closest('[id$="_wrapper"]'), tmp_total = custom_dt.find('.ttotal');
			custom_dt
				.find('.dataTables_filter').find('input').attr({placeholder:'Buscar'}).end().end()
				.find('.itotal').text(tmp_total.text().length>0?' de '+tmp_total.text():'').end();
				//.find('.row:first').find('.col-sm-6').removeClass('col-sm-6').addClass('col-xs-6').eq(0).html(myfilter).end().end().end();
			tmp_total.remove();
		});
 	};
 });