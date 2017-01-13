var global_color;
$(document).on('change', '#color-box', function(){ 
  color_code = $(this).val()
  $('.color_value').find('input').val(color_code);
})
$(document).on('change', '#font-color-box', function(){ 
  font_color_code = $(this).val()
  $('.font_color_value').find('input').val(font_color_code);
})
$(document).on('change', '#contrast-color-box', function(){
  color_code = $(this).val()
  $('.contrast_color_value').find('input').val(color_code);
})
$(document).ready(function(){
	params = {
              jsonrpc:2.0,
              method:"call",
              params:{},
              };
  	$.ajax({ 
	    url : "/get/color",
	    method: "POST",
	    contentType: 'application/json',
	    data: JSON.stringify(params),
	    dataType :"json",
	    success: function(response){
	    	global_ui = response.result;
	    	$('#oe_main_menu_navbar').attr('style', 'background-color:'+global_ui['color']+'');

		}
	  });
	    setInterval(function(){
  			$('.openerp .oe_leftbar .oe_secondary_menus_container').css('font-family', global_ui['font_family']);
	    	$('body').css('font-family', global_ui['font_family']);
	    	$('.openerp .nav-pills li > a').css('color', global_ui['font_color']);
	    	$(".badge").css("background-color", global_ui['color']);
	    	$('.openerp .oe_secondary_menu_section').css("color", global_ui['color']);
	    	$('.openerp .oe_secondary_menu_section').find(".oe_menu_leaf").css("color", global_ui['color']);
	    	$('.o_web_client .openerp .oe_loading').css("color", global_ui['color']);
	    	$('.btn-primary').css("background-color", global_ui['color']);
	    	$('.oe_highlight oe_kanban_action oe_kanban_action_button').css("background-color", global_ui['color']);
	    	$('#oe_main_menu_navbar li a, #oe_main_menu_navbar li button, .navbar-nav li a, .navbar-nav li button').attr('style','font-size:'+global_ui['heading_font_size']+'px !important');
	    	$(".navbar-inverse .navbar-nav>.active>a, .navbar-inverse .navbar-nav>.active>a:focus, .navbar-inverse .navbar-nav>.active>a:hover").attr('style','background-color: green !important');
	    	$(".navbar-inverse .navbar-nav>.active>a, .navbar-inverse .navbar-nav>.active>a:focus, .navbar-inverse .navbar-nav>.active>a:hover").attr('style','background-color:'+global_ui['contrast_color']+' !important');
	    }, 100);
});


$(document).on('click', "#ui_backend_theme", function(){
	debugger;
	    	$('#color-box').val(global_ui['color']);
	    	$('#contrast-color-box').val(global_ui['contrast_color']);
});