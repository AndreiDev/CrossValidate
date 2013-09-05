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
	var Username1_crossFollowing = 0;
	var Username1_crossFollowers = 0;	
	var Username2_crossFollowing = 0;
	var Username2_crossFollowers = 0;	
	var NumOfFetches = 0

	$('#outputUsername1_message').hide("slow");
	$('#outputUsername1').hide("slow");	
	$('#outputUsername2_message').hide("slow");
	$('#outputUsername2').hide("slow");	
	$('#toStep2').hide("slow");
	$('#toStep2_loading').hide("slow");
	$('#toStep2_message').hide("slow");
	$('#stage2').hide("slow");	
	
	// Waiting for rate-limit reset
	function checkRateLimits(data){		
		if (data.waitSeconds > 0){
	   		$('#inputUsername1').prop('disabled', true);
			$('#inputUsername2').prop('disabled', true);	
			$('#inputUsername1').hide("slow");
			$('#inputUsername2').hide("slow");
			$('#subject1go').hide("slow");
			$('#subject2go').hide("slow");		
			var timeToWait = data.waitSeconds;		
			var waitInterval=setInterval(function(){
				if (timeToWait < 1) {
					clearInterval(waitInterval);
					$('#target_stage1').text('Choose key-players in your arena to intersect users that follow them and that they follow');
			   		$('#inputUsername1').prop('disabled', false);
					$('#inputUsername2').prop('disabled', false);	
					$('#inputUsername1').show("slow");
					$('#inputUsername2').show("slow");					
					$('#subject1go').show("slow");
					$('#subject2go').show("slow");													
				}
				else {
					minutes = Math.floor(timeToWait / 60);
					seconds = Math.floor(timeToWait % 60);			
			    	if (minutes < 10) {minutes = "0"+minutes;}
    				if (seconds < 10) {seconds = "0"+seconds;}	
					$('#target_stage1').html('<p>Please wait ' + minutes + ':' + seconds + ' to create another CrossValidate plan <br/> <i>(twitter allows a 15 minutes window per user)</i></p>');		
					timeToWait = timeToWait - 1;
				}		
			},1000);					
		}
		else {			
			$('#target_stage1').text('Choose key-players in your arena to intersect users that follow them and that they follow');
	   		$('#inputUsername1').prop('disabled', false);
			$('#inputUsername2').prop('disabled', false);	
			$('#inputUsername1').show("slow");
			$('#inputUsername2').show("slow");				
			$('#subject1go').show("slow");
			$('#subject2go').show("slow");
		}
	}
	
	if ($('#stage1_header').is(":visible")) {
		Dajaxice.CVapp.AJRateLimit(checkRateLimits,{'resources':['users', 'friends', 'followers']});
	}
	
	function getUser1Stats(data){
		   		
   		$('#inputUsername1').prop('disabled', false);
		$('#inputUsername2').prop('disabled', false);
		$('input[name=outputUsername1_cross]:radio').prop('disabled', false);
		$('input[name=outputUsername2_cross]:radio').prop('disabled', false);		
		$('#subject1go').show("slow");
		$('#subject2go').show("slow");		
		
		if (data.userFollowing){
			userFollowingN = Math.ceil(data.userFollowing / 5000);
			userFollowersN = Math.ceil(data.userFollowers / 5000);
		}		
		if (data.name){
			$('#outputUsername1_name').text(data.name)
			$('#outputUsername1_img').attr('src',data.pic)
			$('#outputUsername1_following').text(data.following)
			$('#outputUsername1_followers').text(data.followers)
			$('#outputUsername1').show("slow");	
			$('#outputUsername1_message').hide("slow");	    	
	    	sub1FollowingN = Math.ceil(data.following / 5000);
	    	sub1FollowersN = Math.ceil(data.followers / 5000);	    
	    	sub1Done = true;
	    	if (sub2Done == true) {
				$('#toStep2').show("slow");
				$('#toStep2_message').hide("slow");
				$('#toStep2_loading').hide("slow");
	    	}	    		    	
	   	}
	   	else if (data.message) {
	   		$('#outputUsername1').hide("slow");	
	   		$('#outputUsername1_message').show("slow");
	   		$('#outputUsername1_message').text(data.message);
	   		sub1Done = false;
			$('#toStep2').hide("slow");
			$('#toStep2_message').hide("slow");
			$('#toStep2_loading').hide("slow");	   		
	   	}
	    else{
	    	$('#outputUsername1').hide("slow");	
	    	$('#outputUsername1_message').hide("slow");
			sub1Done = false;
			$('#toStep2').hide("slow");
			$('#toStep2_message').hide("slow");		
			$('#toStep2_loading').hide("slow");	
		}
	}
	
	$('#subject1go').click(function(){
		$('#toStep2').hide("slow");
		if ($('#inputUsername1').val()=="" || (alphaNumeric.test($('#inputUsername1').val()) && $('#inputUsername1').val().length <= 15)) {
	   		$('#outputUsername1').hide("slow");	
	   		$('#outputUsername1_message').show("slow");
	   			   		
	   		$('#inputUsername1').prop('disabled', true);
			$('#inputUsername2').prop('disabled', true);
			$('input[name=outputUsername1_cross]:radio').prop('disabled', true);
			$('input[name=outputUsername2_cross]:radio').prop('disabled', true);
			$('#subject1go').hide();
			$('#subject2go').hide();	   		
	   		
	   		$('#outputUsername1_message').text('loading...');
	  		Dajaxice.CVapp.AJuserStats(getUser1Stats,{'username':$('#inputUsername1').val(),'field':'subject1'});			
		}
		else {
	   		$('#outputUsername1').hide("slow");	
	   		$('#outputUsername1_message').show("slow");
	   		$('#outputUsername1_message').text('Please enter an alphanumeric username, up to 15 characters');
	   		sub1Done = false;
		}
	});
	
	function getUser2Stats(data){
		
   		$('#inputUsername1').prop('disabled', false);
		$('#inputUsername2').prop('disabled', false);
		$('input[name=outputUsername1_cross]:radio').prop('disabled', false);
		$('input[name=outputUsername2_cross]:radio').prop('disabled', false);	
		$('#subject1go').show();
		$('#subject2go').show();
				
		if (data.userFollowing){
			userFollowingN = Math.ceil(data.userFollowing / 5000);
			userFollowersN = Math.ceil(data.userFollowers / 5000);
		}		
		if (data.name){
			$('#outputUsername2_name').text(data.name)
			$('#outputUsername2_img').attr('src',data.pic)
			$('#outputUsername2_following').text(data.following)
			$('#outputUsername2_followers').text(data.followers)
			$('#outputUsername2').show("slow");	
			$('#outputUsername2_message').hide("slow");	    	
	    	sub2FollowingN = Math.ceil(data.following / 5000);
	    	sub2FollowersN = Math.ceil(data.followers / 5000);	    
	    	sub2Done = true;
	    	if (sub1Done == true) {
				$('#toStep2').show("slow");
				$('#toStep2_message').hide("slow");
				$('#toStep2_loading').hide("slow");
	    	}    	
	   	}
	   	else if (data.message) {
	   		$('#outputUsername2').hide("slow");	
	   		$('#outputUsername2_message').show("slow");
	   		$('#outputUsername2_message').text(data.message);
	   		sub2Done = false;
			$('#toStep2').hide("slow");
			$('#toStep2_message').hide("slow");	
			$('#toStep2_loading').hide("slow");   		
	   	}
	    else{
	    	$('#outputUsername2').hide("slow");	
	    	$('#outputUsername2_message').hide("slow");
			sub2Done = false;
			$('#toStep2').hide("slow");
			$('#toStep2_message').hide("slow");	
			$('#toStep2_loading').hide("slow");		
		}	    	
	}	
	
	$('#subject2go').click(function(){	
		$('#toStep2').hide("slow");	
		if ($('#inputUsername2').val()=="" || (alphaNumeric.test($('#inputUsername2').val()) && $('#inputUsername2').val().length <= 15)) {
	   		$('#outputUsername2').hide("slow");	
	   		
	   		$('#inputUsername1').prop('disabled', true);
			$('#inputUsername2').prop('disabled', true);
			$('input[name=outputUsername1_cross]:radio').prop('disabled', true);
			$('input[name=outputUsername2_cross]:radio').prop('disabled', true);
			$('#subject1go').hide();
			$('#subject2go').hide();			
			
	   		$('#outputUsername2_message').show("slow");
	   		$('#outputUsername2_message').text('loading...');
	  		Dajaxice.CVapp.AJuserStats(getUser2Stats,{'username':$('#inputUsername2').val(),'field':'subject2'});			
		}
		else {
	   		$('#outputUsername2').hide("slow");	
	   		$('#outputUsername2_message').show("slow");
	   		$('#outputUsername2_message').text('Please enter an alphanumeric username, up to 15 characters');
	   		sub2Done = false;
		}
	});	
	
	$("input:radio[name=outputUsername1_cross]").click(function() {
    	outputUsername1_cross = $(this).val();
	});
	
	$("input:radio[name=outputUsername2_cross]").click(function() {
    	outputUsername2_cross = $(this).val();
	});		
	
	function openStage2(data){
		if (data.result == 1){			
			$('#toStep2').hide("slow");
			$('#toStep2_loading').hide("slow");
			$('#toStep2_message').hide("slow");	
			$('#stage1').hide("slow");
			$('#stage2').show("slow");	
			$('#crossNum').text(data.crossNum);
			$('#Following_Minimum').val(data.P_minFriends);
			$('#Following_Maximum').val(data.P_maxFriends);
			$('#Followers_Minimum').val(data.P_minFollowers);
			$('#Followers_Maximum').val(data.P_maxFollowers);
			$('#FF_Minimum').val(data.P_minFFratio);
			$('#FF_Maximum').val(data.P_maxFFratio);
			$('#minNoTweets').val(data.P_minNoTweets);
			$('#maxDays').val(data.P_maxDays);
			$('#validationDays').val(data.P_validationDays);
			$('#validationThreshold').val(data.P_validationThreshold);	
		}
		else if (data.result == 0){			
			$('#toStep2').show("slow");
			$('#toStep2_loading').hide("slow");
			$('#toStep2_message').text('Please try again in 15 minutes');
			$('#toStep2_message').show("slow");
			setTimeout(function(){window.location.reload();},5000)
		}		   	
		else if (data.result == 2){
			$('#inputUsername2').prop('disabled', true);
			$('#inputUsername1').prop('disabled', true);
			$('input[name=outputUsername1_cross]:radio').prop('disabled', true);
			$('input[name=outputUsername2_cross]:radio').prop('disabled', true);
			$('#subject1go').hide("slow");
			$('#subject2go').hide("slow");				
			$('#toStep2').hide("slow");
			$('#toStep2_loading').hide("slow");
			$('#toStep2_message').html('<p>No users found in the intersection.<br/> Please choose users that are somehow related to one another, and try again in 15 minutes</p>');
			$('#toStep2_message').show("slow");		
			setTimeout(function(){window.location.reload();},5000)
		}
	}		
	
	$('#toStep2').click(function(){	
		
		if (outputUsername1_cross=="both") {
			Username1_crossFollowing = 1;
			Username1_crossFollowers = 1;			
		}
		else if (outputUsername1_cross=="following"){
			Username1_crossFollowing = 1;
			Username1_crossFollowers = 0;					
		}
		else if (outputUsername1_cross=="followers"){
			Username1_crossFollowing = 0;
			Username1_crossFollowers = 1;					
		}	
		if (outputUsername2_cross=="both") {
			Username2_crossFollowing = 1;
			Username2_crossFollowers = 1;			
		}
		else if (outputUsername2_cross=="following"){
			Username2_crossFollowing = 1;
			Username2_crossFollowers = 0;					
		}
		else if (outputUsername2_cross=="followers"){
			Username2_crossFollowing = 0;
			Username2_crossFollowers = 1;					
		}	
		NumOfFetches = userFollowingN+userFollowersN+sub1FollowingN*Username1_crossFollowing+sub1FollowersN*Username1_crossFollowers+sub2FollowingN*Username2_crossFollowing+sub2FollowersN*Username2_crossFollowers;
		if (NumOfFetches <= 15) {
			$('#inputUsername1').prop('disabled', true);
			$('#inputUsername2').prop('disabled', true);
			$('input[name=outputUsername1_cross]:radio').prop('disabled', true);
			$('input[name=outputUsername2_cross]:radio').prop('disabled', true);
			$('#subject1go').hide("slow");
			$('#subject2go').hide("slow");	
			$('#step1').hide("slow");	
			$('#toStep2_message').hide("slow");
			$('#toStep2').hide("slow");
			$('#toStep2_loading').show("slow");
			
			Dajaxice.CVapp.AJgetCrossUsers(openStage2,{'Username1_crossFollowing':Username1_crossFollowing,'Username1_crossFollowers':Username1_crossFollowers,'Username2_crossFollowing':Username2_crossFollowing,'Username2_crossFollowers':Username2_crossFollowers});			

		} 
		else {
			$('#toStep2').show("slow");
			$('#toStep2_loading').hide("slow");
			$('#toStep2_message').text('Number of fetches exceeded (' + NumOfFetches +')');
			$('#toStep2_message').show("slow");			
		}
	});		

	function refreshCrossNum(data){
		$('#crossNum').text(data.crossNum);
	};
	
	function reCalculate(){
    	$("body").css("cursor", "progress");		
    	Dajaxice.CVapp.AJrecalculate(refreshCrossNum,{
    	'Following_Minimum':$('#Following_Minimum').val(),
    	'Following_Maximum':$('#Following_Maximum').val(),
    	'Followers_Minimum':$('#Followers_Minimum').val(),
    	'Followers_Maximum':$('#Followers_Maximum').val(),
    	'FF_Minimum':$('#FF_Minimum').val(),
    	'FF_Maximum':$('#FF_Maximum').val(),
    	'minNoTweets':$('#minNoTweets').val(),
    	'maxDays':$('#maxDays').val()}    	   	
    	);
    	$("body").css("cursor", "default"); 
    };		
	
	$('#stage2 select').change(function(){
		reCalculate();
	});
    
	function openStage3(data){
		if (data.result){			
			location.reload();
		}
		else {

		}		   	
	}		    
    
    $('#toStep3').click(function(){
    	Dajaxice.CVapp.AJselectUsers(openStage3,{
    	'Following_Minimum':$('#Following_Minimum').val(),
    	'Following_Maximum':$('#Following_Maximum').val(),
    	'Followers_Minimum':$('#Followers_Minimum').val(),
    	'Followers_Maximum':$('#Followers_Maximum').val(),
    	'FF_Minimum':$('#FF_Minimum').val(),
    	'FF_Maximum':$('#FF_Maximum').val(),
    	'minNoTweets':$('#minNoTweets').val(),
    	'maxDays':$('#maxDays').val(),
    	'validationDays':$('#validationDays').val(),
    	'validationThreshold':$('#validationThreshold').val()}
    	)
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