$(window).load(function() {

	var $search = $('.navbar-search');
	var $button = $('a', $search);
	var $input = $('input', $search);
	var url = $button.attr("href");
	
	$button.click(onSearch);
	$('form', $search).submit(onSearch);
	
	function onSearch() {
		
		var value = $input[0].value;
		value = value.replace(/^\s+|\s+$/gm,'');
		
		if (value != "") url += "?q="+encodeURIComponent(value);
		window.location.href = url;
		
		return false;
	}
})