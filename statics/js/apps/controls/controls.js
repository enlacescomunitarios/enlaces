/*!
 * auhtor: Luis Eduardo Miranda Barja
 * (C) 2015 - mbarjaedu13@gmail.com
 */
$(function(){
	$('.pregnant-menu').addClass('active');
	var o_key = $('#breadcrumbs').data('key');
	$('#breadcrumbs').removeAttr('data-key');
	$('.back').on({
		click:function(e){
			e.preventDefault();
			location.href='/embarazos/gestion?id_per='+o_key.id_per;
		}
	});
	$('.born').on({
		click:function(e){
			e.preventDefault();
			location.href='/embarazos/reg_parto?id_emb='+o_key.id_emb;
		}
	});
	$('.interrupt').on({
		click:function(e){
			e.preventDefault();
			location.href='/embarazos/interrumpir?id_emb='+o_key.id_emb;
		}
	});
	$('.confirm').on({
		click:function(e){
			e.preventDefault();
			location.href='/embarazos/conf_interr?id_emb='+o_key.id_emb;
		}
	});
	$('#custom').customPaginator();
});