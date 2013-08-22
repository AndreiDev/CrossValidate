$(document).ready(function () {	
	var alphaNumeric = /^[a-zA-Z0-9_]+$/;
		
	function getUser1Stats(data){
		if (data.name){
	    	$('#outputUsername1').replaceWith('<div id="outputUsername1"><p>'+data.name+'</p><img src="'+data.pic+'"></img> <p>'+data.message+'</p></div>');
	   	}
	   	else if (data.message) {
	   		$('#outputUsername1').replaceWith('<div id="outputUsername1"><p>'+data.message+'</p></div>');
	   	}
	    else{
			$('#outputUsername1').replaceWith('<div id="outputUsername1"></div>')
		}
	}
	
	function getUser2Stats(data){
		if (data.name){
	    	$('#outputUsername2').replaceWith('<div id="outputUsername2"><p>'+data.name+'</p><img src="'+data.pic+'"></img> <p>'+data.message+'</p></div>');
	   	}
	   	else if (data.message) {
	   		$('#outputUsername2').replaceWith('<div id="outputUsername2"><p>'+data.message+'</p></div>');
	   	}	   	
	    else {
			$('#outputUsername2').replaceWith('<div id="outputUsername2"></div>')
		}	    	
	}	
	
	$('#inputUsername1').focusout(function(){
		if ($('#inputUsername1').val()=="" || (alphaNumeric.test($('#inputUsername1').val()) && $('#inputUsername1').val().length < 15)) {
			$('#outputUsername1').replaceWith('<div id="outputUsername1"><p>Loading...</p></div>');
	  		Dajaxice.CVapp.AJuserStats(getUser1Stats,{'username':$('#inputUsername1').val(),'field':'subject1'});			
		}
		else {
			$('#outputUsername1').replaceWith('<div id="outputUsername1"><p>Please enter an alphanumeric username up to 15 characters</p></div>');
			$('#inputUsername1').val('')
		}
	});
	
	$('#inputUsername2').focusout(function(){		
		if ($('#inputUsername2').val()=="" || (alphaNumeric.test($('#inputUsername2').val()) && $('#inputUsername2').val().length < 15)) {
			$('#outputUsername2').replaceWith('<div id="outputUsername2"><p>Loading...</p></div>');
	  		Dajaxice.CVapp.AJuserStats(getUser2Stats,{'username':$('#inputUsername2').val(),'field':'subject2'});			
		}
		else {
			$('#outputUsername2').replaceWith('<div id="outputUsername2"><p>Please enter an alphanumeric username up to 15 characters</p></div>');
			$('#inputUsername2').val('')
		}
	});	
	
	$('#pleaseWait').submit(function() {
    	window.setTimeout('location.reload()', 500);
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