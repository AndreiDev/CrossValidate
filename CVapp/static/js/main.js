$(document).ready(function () {	
	var alphaNumeric = /^[a-zA-Z0-9_]+$/;
	var sub1Done = false;
	var sub2Done = false;
	var userFollowingN = 0;
	var userFollowersN = 0;
	var sub1FollowingN = 0;
	var sub1FollowersN = 0;
	var sub2FollowingN = 0;
	var sub2FollowersN = 0;
	var outputUsername1_cross = "both";
	var outputUsername2_cross = "both";

	$('#outputUsername1_message').hide();
	$('#outputUsername1').hide();	
	$('#outputUsername2_message').hide();
	$('#outputUsername2').hide();	
	
	function getUser1Stats(data){
		if (data.userFollowing){
			userFollowingN = Math.ceil(data.userFollowing / 5000);
			userFollowersN = Math.ceil(data.userFollowers / 5000);
		}		
		if (data.name){
			$('#outputUsername1_name').text(data.name)
			$('#outputUsername1_img').attr('src',data.pic)
			$('#outputUsername1_following').text(data.following)
			$('#outputUsername1_followers').text(data.followers)
			$('#outputUsername1').show();	
			$('#outputUsername1_message').hide();	    	
	    	sub1FollowingN = Math.ceil(data.following / 5000);
	    	sub1FollowersN = Math.ceil(data.followers / 5000);	    
	    	sub1Done = true;
	   	}
	   	else if (data.message) {
	   		$('#outputUsername1').hide();	
	   		$('#outputUsername1_message').show();
	   		$('#outputUsername1_message').text(data.message);
	   		sub1Done = false;
	   	}
	    else{
	    	$('#outputUsername1').hide();	
	    	$('#outputUsername1_message').hide();
			sub1Done = false;
		}
	}
	
	function getUser2Stats(data){
		if (data.userFollowing){
			userFollowingN = Math.ceil(data.userFollowing / 5000);
			userFollowersN = Math.ceil(data.userFollowers / 5000);
		}		
		if (data.name){
			$('#outputUsername2_name').text(data.name)
			$('#outputUsername2_img').attr('src',data.pic)
			$('#outputUsername2_following').text(data.following)
			$('#outputUsername2_followers').text(data.followers)
			$('#outputUsername2').show();	
			$('#outputUsername2_message').hide();	    	
	    	sub2FollowingN = Math.ceil(data.following / 5000);
	    	sub2FollowersN = Math.ceil(data.followers / 5000);	    
	    	sub2Done = true;
	   	}
	   	else if (data.message) {
	   		$('#outputUsername2').hide();	
	   		$('#outputUsername2_message').show();
	   		$('#outputUsername2_message').text(data.message);
	   		sub2Done = false;
	   	}
	    else{
	    	$('#outputUsername2').hide();	
	    	$('#outputUsername2_message').hide();
			sub2Done = false;
		}	    	
	}	
	//$('#outputUsername1_cross').find(":selected").text()
	$('#subject1go').click(function(){
		if ($('#inputUsername1').val()=="" || (alphaNumeric.test($('#inputUsername1').val()) && $('#inputUsername1').val().length < 15)) {
	   		$('#outputUsername1').hide();	
	   		$('#outputUsername1_message').show();
	   		$('#outputUsername1_message').text('loading...');
	  		Dajaxice.CVapp.AJuserStats(getUser1Stats,{'username':$('#inputUsername1').val(),'field':'subject1'});			
		}
		else {
	   		$('#outputUsername1').hide();	
	   		$('#outputUsername1_message').show();
	   		$('#outputUsername1_message').text('Please enter an alphanumeric username up to 15 characters');
	   		sub1Done = false;
		}
	});
	
	$('#subject2go').click(function(){		
		if ($('#inputUsername2').val()=="" || (alphaNumeric.test($('#inputUsername2').val()) && $('#inputUsername2').val().length < 15)) {
	   		$('#outputUsername2').hide();	
	   		$('#outputUsername2_message').show();
	   		$('#outputUsername2_message').text('loading...');
	  		Dajaxice.CVapp.AJuserStats(getUser2Stats,{'username':$('#inputUsername2').val(),'field':'subject2'});			
		}
		else {
	   		$('#outputUsername2').hide();	
	   		$('#outputUsername2_message').show();
	   		$('#outputUsername2_message').text('Please enter an alphanumeric username up to 15 characters');
	   		sub2Done = false;
		}
	});	
	
	$("input:radio[name=outputUsername1_cross]").click(function() {
    	outputUsername1_cross = $(this).val();
	});
	
	$("input:radio[name=outputUsername2_cross]").click(function() {
    	outputUsername2_cross = $(this).val();
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