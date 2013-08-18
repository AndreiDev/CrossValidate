from django import forms
from CVapp.models import Job, FollowBack

class jobForm_step1(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('subject1Name','subject2Name')
        
class jobForm_step2(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('P_crossType',)   

class jobForm_step3(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('P_minFollowers','P_maxFollowers','P_minFriends','P_maxFriends','P_minFFratio','P_maxFFratio','P_minNoTweets','P_maxDays')
        
class jobForm_step4(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('P_unfollowAfter','P_testAfter','P_validationThreshold')        
