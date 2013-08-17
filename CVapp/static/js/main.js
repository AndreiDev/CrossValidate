$(document).ready(function () {
	
	$('#pleaseWait').submit(function() {
    $('#pleaseWait').replaceWith('<h2>Please Wait...</h2>');
  });
	// media query event handler
	if (matchMedia) {
		var mq = window.matchMedia("(max-width: 767px)");
		mq.addListener(WidthChange);
		WidthChange(mq);
	}
	// media query change
	function WidthChange(mq) {
		if (mq.matches) {
			// window width is at most 767px

		}
		else {
			// window width is more than 767px
			
		}
	}

});