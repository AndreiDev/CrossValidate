from django import forms
from CVapp.models import Job, FollowBack

class jobForm_step1(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('jobStep','userName','interactionDateTime','P_crossType','P_minFollowers','P_maxFollowers','P_minFriends','P_maxFriends','P_maxDays','P_unfollowAfter','P_testAfter','P_validationThreshold')
