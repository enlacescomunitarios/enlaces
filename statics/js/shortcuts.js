/*!
 * auhtor: Luis Eduardo Miranda Barja
 * (C) 2015 - mbarjaedu13@gmail.com
 */
$(function(){
	getCookie = function(name) {
		var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
		return r ? r[1] : undefined;
	};
	var patterns = {
			login: /^(?:[^\s]{6,12})$/,
			passwd: /^(?=[^\t\n\v\f\r ]*?[A-Z])(?=[^\t\n\v\f\r ]*?[a-z])(?=[^\t\n\v\f\r ]*?[0-9])[^\t\n\v\f\r ]{6,12}$/,
	 		ci: /^(?:[1-9][0-9]{6}[A-Z]?)$/i,
	 		//p_names: /^(?:(?:\b[A-ZÁÉÍÓÚÄËÏÖÜÑ](?:'[A-Z])?[a-záéíóúäëïöüñ]+ ?\b){1,4})$/i,
	 		p_names: /^(?:(?:\b[A-ZÁÉÍÓÚÄËÏÖÜÑ](?:'[A-Z])?[a-záéíóúäëïöüñ]+ ?){1,4})$/i,
	 		//p_lastnames: /^(?:(?:\b(?: ?[Dd]el? ?)?(?: ?La ?)?(?: ?v[ao]n ?)?\b[A-ZÁÉÍÓÚÄËÏÖÜÑ](?:'[A-Z])?[a-záéíóúäëïöüñ]+ ?\b){1,2})$/i,
	 		p_lastnames: /^(?:(?:\b(?: ?[Dd]el? ?)?(?: ?La ?)?(?: ?v[ao]n ?)?\b[A-ZÁÉÍÓÚÄËÏÖÜÑ](?:'[A-Z])?[a-záéíóúäëïöüñ]+ ?){1,2})$/i,
	 		//profession: /^(?:(?:[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\.?(?:(?: [A-Z]+)?(?: ?[Dd]el?)?(?: ?[Ll][ao]s?)?(?: ?en)?)? ?)+)$/,
	 		//profession: /^(?:(?:[A-ZÁÉÍÓÚÄËÏÖÜÑ][a-záéíóúäëïöüñ]+\.?(?:(?: [A-Z]+)?(?: ?[Dd]el?)?(?: ?[Ll][ao]s?)?(?: ?en)?)? ?)+)$/i,
	 		profession: /^(?:(?:\b[A-ZÁÉÍÓÚÄËÏÖÜÑ][a-záéíóúäëïöüñ]+(?:(?:\.? [A-Z]+)?(?: ?[Dd]el?)?(?: ?[Ll][ao]s?)?(?: ?en)?)? ?)+)$/i,
	 		//date: /^(?:(((19|20)[0-9]{2})-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])))$/,
	 		date: /^(?:((0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[012])\/((19|20)[0-9]{2})))$/,
	 		time: /^(?:(?:[0-1][0-9]|2[0-3])(?::(?:[0-5][0-9])){1,2})$/,
	 		cell_phone: /^(?:[6-7][0-9]{7})$/,
	 		g_names: /^(?:(?:[A-ZÁÉÍÓÚÑ](?:'[A-Z])?[a-záéíóúäëïöüñ]+(?:(?:\.? ?[1-9][0-9]*)?(?: ?[Ee]n)?(?: ?[Dd]el?)?(?: ?[Ll][ao]s?)?)? ?)+)$/i,
	 		neonato_weight: /^(?:[1-5]\b(?:\.?[0-9]{1,3})?)$/,
	 		msg_number: /^(?:[1-9][0-9]?){1}$/,
	 		msg_content: /^(?:[^\s] ?){2,}$/i,
	 		comments: /^(?:[^\s] ?){2,}$/i,
	 	},
	 	pattern_name = function(obj){
	 		//var __tmp = obj.prop('class').match("^(?:(?:[^w]+ ?)?only_(?:([a-z_]+)))$");
	 		var __tmp = obj.prop('class').match(/(?:(?:(?: ?[a-z]-? ?)+)?(?:only_((?:[a-z]_?)+))(?:(?: ?[a-z]-? ?)+)?)/);
	 		return __tmp!=null?__tmp[1]:null;
	 	},
	 	warnings = function(obj){
	 		var success = true,
	 			fields = obj==null?$('form :input[class*="only_"]:enabled'):[]
	 			c_alert = function(obj, success){
	 				if(obj.val().match(ptr) != null && obj.closest('.form-group').hasClass('fail-check')==false){
	 					obj.closest('.form-group').removeClass('has-error').addClass('has-success').find('.form-control-feedback').removeClass('fa-times').addClass('fa fa-check');
	 				} else{
	 					if(!obj.prop('required') && obj.val().length==0){
	 						obj.closest('.form-group').removeClass('has-error').removeClass('has-success').find('.form-control-feedback').removeClass('fa-times').addClass('fa fa-check');
	 					} else{
	 						success = success==true?false:success;
	 						obj.closest('.form-group').removeClass('has-success').addClass('has-error').find('.form-control-feedback').removeClass('fa-check').addClass('fa fa-times');
	 					}
	 				}
	 				return success;
	 			};
	 		if(obj!=null){
	 			var ptr = patterns[pattern_name(obj)];
	 			//console.log(obj.val().match(ptr));
	 			success = c_alert(obj, success);
	 		} else{
	 			for (var i = 0; i < fields.length; i++) {
	 				var obj = $(fields[i]), ptr = patterns[pattern_name(obj)];
	 				success = c_alert(obj, success);
	 			}
	 		}
	 		return success;
	 	};
	check_inputs = function(){
		var success = warnings(),
			fields = $('form select:enabled');
		for (var i = 0; i < fields.length; i++) {
			var obj = $(fields[i]);
			//console.dir(obj);
			//console.log(obj.prop('type')=='textarea');
			if(+obj.val() == -1 && obj.prop('required')){
				obj.closest('.form-group').removeClass('has-success').addClass('has-error');
				success = success==true?false:success;
			} else{
				obj.closest('.form-group').removeClass('has-error').addClass('has-success');
			}
		}
		return success;
	};
	$('form').on('click focus keyup blur', ':input[class*="only_"]:enabled', function(e){
		var obj = $(this);
		if(e.type=='focusout'){
			obj.val(obj.val().trim());
		}
		//console.log($.type(obj.data('pattern')));
		if($.type(obj.data('pattern'))=='undefined'){
			var ptrn = patterns[pattern_name(obj)];
			obj.data('pattern', ptrn);
		} else{
			warnings(obj);
		}
	}).on('change','select:enabled', function(e){
		//check_inputs();
		var obj = $(this);
		if(obj.prop('type')=='select-one'){
			if(+obj.val() == -1 && obj.prop('required')){
				obj.closest('.form-group').removeClass('has-success').addClass('has-error');
				//success = success==true?false:success;
			} else{
				obj.closest('.form-group').removeClass('has-error').addClass('has-success');
			}
		}
	}).find('button[type=submit]').on({
		click:function(e){
			e.preventDefault();
			e.stopPropagation();
			var o_form = $('form'), success = check_inputs(), btn_submit = $(this);
			//console.log('form status: '+success);
			if(success){
				btn_submit.disable();
				o_form.submit();
			} else{
				//alert('Por favor, corrija los campos marcados en rojo.!');
				o_form.find(':input:enabled').each(function(){
					var o_input = $(this);
					//console.log(o_input.closest('fieldset').hasClass('has-error'));
					if(o_input.closest('.form-group').hasClass('has-error')){
						o_input.tooltip({
							//'trigger':'hover',
							'placement':'bottom',
							'title':'Corrija éste campo..!',
							//'container':'body',
							//'show':true,
						}).tooltip('show').on({
							click:function(e){
								$(this).tooltip('destroy');
							}
						});
					}
				});
			}
		}
	});
	$.fn.disable = function(){
		this.enable(false);
		return this;
	};
	$.fn.enable = function(opt_enable){
		//console.log(arguments);
		var tmp_obj = $(this);
		//console.log('doms: '+tmp_obj.size());
		if(arguments.length && !opt_enable){
			//this.attr("disabled","disabled");
			if(tmp_obj.size()==1){
				tmp_obj.attr("disabled","disabled").find(':input').attr("disabled","disabled").end();
			} else{
				$.each(tmp_obj, function(){
					$(this).attr("disabled","disabled").find(':input').attr("disabled","disabled").end();
				});
			}
		} else{
			if(tmp_obj.size()==1){
				tmp_obj.removeAttr("disabled").find(':input').removeAttr("disabled").end();
			} else{
				$.each(tmp_obj, function(){
					$(this).removeAttr("disabled").find(':input').removeAttr("disabled");
				});
			}
		}
		return tmp_obj;
	};
	$.fn.form2Dict = function(opt){
		if(arguments.length && opt){
			return this.serializeArray();
		} else{
			var obj = new Object();
			$.each(this.serializeArray(), function(k,v){
				obj[v.name] = v.value;
			});
			return obj;
		}
	};
});