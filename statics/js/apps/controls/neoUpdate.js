/*!
 * auhtor: Luis Eduardo Miranda Barja
 * (C) 2015 - mbarjaedu13@gmail.com
 */
$(function(){
	var o_key = $('#breadcrumbs').data('key');
	$('#breadcrumbs').removeAttr('data-key');
	$('.pregnants').on({
		click:function(e){
			e.preventDefault();
			location.href='/embarazadas/gestion';
		}
	});
	$('.pregnant').on({
		click:function(e){
			e.preventDefault();
			location.href='/embarazos/gestion?id_per='+o_key.id_per;
		}
	});
	$('.back').on({
		click:function(e){
			e.preventDefault();
			location.href='/controles/gestion?id_rcn='+o_key.id_rcn;
		}
	});
	$('form').on({
		submit:function(e){
			e.preventDefault();
			var oform = $(this), btn_submit = $('button[type=submit]');
			btn_submit.disable().hide();
		}
	});
});