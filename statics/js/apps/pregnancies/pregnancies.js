/*!
 * auhtor: Luis Eduardo Miranda Barja
 * (C) 2015 - mbarjaedu13@gmail.com
 */
$(function(){
	$('.pregnant-menu').addClass('active');
	$('.back').on({
		click:function(e){
			e.preventDefault();
			location.href='/embarazadas/gestion';
		}
	});
	var o_key = $('#breadcrumbs').data('key');
	$('.edit').on({
		click:function(e){
			e.preventDefault();
			location.href='/embarazadas/modificar_embarazada?id_per='+o_key;
		}
	});
	$('.pregnancy').on({
		click:function(e){
			e.preventDefault();
			location.href="/embarazos/nuevo_embarazo?id_per="+o_key;
		}
	});
	$('.confirm').on({
		click:function(e){
			e.preventDefault();
			location.href='/embarazadas/conf_defuncion?id_per='+o_key;
		}
	});
	$('.death_reg').on({
		click:function(e){
			e.preventDefault();
			location.href='/embarazadas/defuncion?id_per='+o_key;
		}
	});
	$('.pregDisable').on({
		click:function(e){
			e.preventDefault();
			swal({
				title: 'Advertencia!',
				text: 'Está seguro?',
				type: 'warning',
				showCancelButton: true,
				cancelButtonText: "Cancelar",
				cancelButtonClass: 'btn-warning',
				confirmButtonText: "Confirmar",
				confirmButtonClass: 'btn-primary',
				closeOnConfirm: true
			}, function(){
				$.post(
					'/embarazadas/eliminar',
					data = {'_xsrf':getCookie('_xsrf'),'id_per':o_key},
					function(response){
						if(!response){
							location.href='/embarazos/gestion?id_per='+o_key;
						}
					}
				);
			});
		}
	});
	$('#custom, #neo-natos').customPaginator({range:[3,5]});
	//$('#neo-natos').customPaginator({height:'auto',range:[3,5]});
});