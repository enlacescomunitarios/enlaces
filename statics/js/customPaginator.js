/*!
 * auhtor: Luis Eduardo Miranda Barja
 * (C) 2014 - mbarjaedu13@gmail.com
 */
$(function(){
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
		return this.each(function(){
			var o_table = $(this);
			o_table.find('tbody').find('a, .link').each(function(){
				var olink = $(this);
				olink.data('link', olink.attr('href')).removeAttr('href').on({
					click:function(e){
						e.preventDefault();
						location.href = $(this).data('link');
					}
				});
			});
			var custom_dt = o_table.dataTable($cfg).closest('[id$="_wrapper"]'), tmp_total = custom_dt.find('.ttotal');
			custom_dt
				.find('.dataTables_filter').find('input').attr({placeholder:'Buscar'}).end().end()
				.find('.itotal').text(tmp_total.text().length>0?' de '+tmp_total.text():'').end();
			//tmp_total.remove();
		});
	};
	$.fn.cfilter = function(data_list){
		var o_select = $('<select class="form-control input-sm cfilter"/>'), list_options = ['<option value="-1">Todo</option>'];
		for(var i in data_list){
			var obj = data_list[i], o_op = $('<option/>');
			o_op.attr({'value':obj.val,'selected':(obj.def==true?true:false)}).text(obj.label);
			list_options.push(o_op);
		};
		o_select.html(list_options);
		return this.each(function(){
			var custom_dt = $(this).closest('[id$="_wrapper"]');
			custom_dt
				.find('.row:first').find('.col-sm-6').removeClass('col-sm-6').addClass('col-xs-6').eq(0).html(o_select).end().end().end()
				.find('.dataTables_filter').find('input').val(o_select.val()=='-1'?'':o_select.val()).keyup().end().end();
			var o_total = custom_dt.find('.ttotal').text();
			custom_dt.find('.itotal').text(o_total.length>0?' de '+o_total:'').end();
			o_select.on({
				change:function(e){
					var o_str = $(this).val();
					custom_dt.find('.dataTables_filter').find('input').val(o_str=='-1'?'':o_str).keyup().end().end();
					var tmp_total = custom_dt.find('.ttotal').text();
					custom_dt.find('.itotal').text(tmp_total.length>0?' de '+tmp_total:'').end();
				}
			});
		});
	};
});