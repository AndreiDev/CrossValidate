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
	var outputUsername1_crossFollowing = 0;
	var outputUsername1_crossFollowers = 0;	
	var outputUsername2_crossFollowing = 0;
	var outputUsername2_crossFollowers = 0;	
	var NumOfFetches = 0

	$('#outputUsername1_message').hide();
	$('#outputUsername1').hide();	
	$('#outputUsername2_message').hide();
	$('#outputUsername2').hide();	
	$('#toStep2').hide();
	$('#toStep2_message').hide();
	
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
	    	if (sub2Done == true) {
				$('#toStep2').show();
				$('#toStep2_message').show();	
	    	}	    		    	
	   	}
	   	else if (data.message) {
	   		$('#outputUsername1').hide();	
	   		$('#outputUsername1_message').show();
	   		$('#outputUsername1_message').text(data.message);
	   		sub1Done = false;
			$('#toStep2').hide();
			$('#toStep2_message').hide();	   		
	   	}
	    else{
	    	$('#outputUsername1').hide();	
	    	$('#outputUsername1_message').hide();
			sub1Done = false;
			$('#toStep2').hide();
			$('#toStep2_message').hide();			
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
	    	if (sub1Done == true) {
				$('#toStep2').show();
				$('#toStep2_message').show();	
	    	}    	
	   	}
	   	else if (data.message) {
	   		$('#outputUsername2').hide();	
	   		$('#outputUsername2_message').show();
	   		$('#outputUsername2_message').text(data.message);
	   		sub2Done = false;
			$('#toStep2').hide();
			$('#toStep2_message').hide();	   		
	   	}
	    else{
	    	$('#outputUsername2').hide();	
	    	$('#outputUsername2_message').hide();
			sub2Done = false;
			$('#toStep2').hide();
			$('#toStep2_message').hide();			
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
	
	$('#toStep2').click(function(){	
		
		if (outputUsername1_cross=="both") {
			outputUsername1_crossFollowing = 1;
			outputUsername1_crossFollowers = 1;			
		}
		else if (outputUsername1_cross=="following"){
			outputUsername1_crossFollowing = 1;
			outputUsername1_crossFollowers = 0;					
		}
		else if (outputUsername1_cross=="followers"){
			outputUsername1_crossFollowing = 0;
			outputUsername1_crossFollowers = 1;					
		}	
		if (outputUsername2_cross=="both") {
			outputUsername2_crossFollowing = 1;
			outputUsername2_crossFollowers = 1;			
		}
		else if (outputUsername2_cross=="following"){
			outputUsername2_crossFollowing = 1;
			outputUsername2_crossFollowers = 0;					
		}
		else if (outputUsername2_cross=="followers"){
			outputUsername2_crossFollowing = 0;
			outputUsername2_crossFollowers = 1;					
		}	
		NumOfFetches = userFollowingN+userFollowersN+sub1FollowingN*outputUsername1_crossFollowing+sub1FollowersN*outputUsername1_crossFollowers+sub2FollowingN*outputUsername2_crossFollowing+sub2FollowersN*outputUsername2_crossFollowers;
		if (NumOfFetches <= 15) {
			$('#inputUsername2').prop('disabled', true);
			$('#inputUsername1').prop('disabled', true);
			$('input[name=outputUsername1_cross]:radio').prop('disabled', true);
			$('input[name=outputUsername2_cross]:radio').prop('disabled', true);
			$('#subject1go').hide();
			$('#subject2go').hide();
			$('#toStep2').hide();			
			$('#toStep2_message').hide();
			
			
		} 
		else {
			$('#toStep2').show();
			$('#toStep2_message').text('Number of fetches exceeded (' + NumOfFetches +')');
			$('#toStep2_message').show();			
		}
	});	
	
	$("input:radio[name=outputUsername1_cross]").click(function() {
    	outputUsername1_cross = $(this).val();
	});
	
	$("input:radio[name=outputUsername2_cross]").click(function() {
    	outputUsername2_cross = $(this).val();
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