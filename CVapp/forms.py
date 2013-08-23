from django import forms
from CVapp.models import Job, CrossData
    
class jobForm_step1_subjects(forms.ModelForm):
    subject1Name = forms.CharField(label="twitter username: ",widget=forms.TextInput(attrs={'placeholder':'enter twitter username', 'id':'inputUsername1'}))
    subject2Name = forms.CharField(label="twitter username: ",widget=forms.TextInput(attrs={'placeholder':'enter twitter username', 'id':'inputUsername2'}))
    
    class Meta:
        model = Job
        
class jobForm_step2_crossType(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('P_crossType',)   

class jobForm_step3_params(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('P_minFollowers','P_maxFollowers','P_minFriends','P_maxFriends','P_minFFratio','P_maxFFratio','P_minNoTweets','P_maxDays')

#class jobForm_step4_followUsers(forms.ModelForm):
#    class Meta:
#        model = CrossData
#        fields = ('screenName','description','imageLink','statusesCount','followersCount','friendsCount','toFollow')             

class jobForm_step5_valParams(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('P_validationDays','P_validationThreshold')   