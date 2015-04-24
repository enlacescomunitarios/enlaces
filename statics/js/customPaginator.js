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
 		var optFields = function(range){
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
 		};
 		var tmp_dataTable = this.dataTable({
	 			//scrollY: 300,
	 			scrollX: true,
	 			sScrollY: (arguments.length && 'height' in config)?config.height:278,
	 			//sScrollX: 599,
	 			/*pagingType:'simple_numbers',//'full_numbers'*/
	 			pagingType: 'full_numbers',
	 			sort: true,
	 			//lengthMenu: arguments.length==0?optFields():optFields(start,stop,step),
	 			lengthMenu: (arguments.length && 'range' in config && config.range.length)?optFields(config.range):optFields(),
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
	 		}).closest('[id$="_wrapper"]').find('.dataTables_filter').find('input').attr({placeholder:'Buscar'}),
			tmp_total = tmp_dataTable.closest('[id$="_wrapper"]').find('.ttotal');
		tmp_dataTable.closest('[id$="_wrapper"]').find('.itotal').text(tmp_total.text().length>0?' de '+tmp_total.text():'');
		tmp_total.remove();
		return tmp_dataTable;
 	};
 });