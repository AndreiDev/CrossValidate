from django.db import models

class Job(models.Model):
    jobDateTime = models.DateTimeField(auto_now_add=True)
    jobStep = models.IntegerField(editable=False)
    userName = models.CharField(max_length=200)
    userFollowersIdsList = models.TextField(max_length=50000,default='',editable=False)
    userFriendsIdsList = models.TextField(max_length=50000,default='',editable=False)
    subject1Name = models.CharField(max_length=200,default='')
    subject1FollowersIdsList = models.TextField(max_length=50000,default='',editable=False)
    subject1FriendsIdsList = models.TextField(max_length=250000,default='',editable=False)
    subject2Name = models.CharField(max_length=200,default='')
    subject2FollowersIdsList = models.TextField(max_length=50000,default='',editable=False)
    subject2FriendsIdsList = models.TextField(max_length=250000,default='',editable=False)    
    crossIds = models.TextField(max_length=5000,default='',editable=False)
    crossUsersRelevantData = models.TextField(max_length=500000,default='',editable=False)
    crossUsersFilteredData = models.TextField(max_length=500000,default='',editable=False)
    P_crossType = models.IntegerField(default=0)
    P_minFollowers = models.IntegerField(default=500)
    P_maxFollowers = models.IntegerField(default=30000)
    P_minFriends = models.IntegerField(default=200)
    P_maxFriends = models.IntegerField(default=30000) 
    P_maxDays = models.IntegerField(default=7)
    P_unfollowAfter = models.IntegerField(default=10)
    P_testAfter = models.IntegerField(default=5)
    P_validationThreshold = models.IntegerField(default=0.5) 
    
    def __unicode__(self):
        return self.userName + ':' + str(self.jobDateTime)
    
class FollowBack(models.Model):
    job = models.ForeignKey(Job)
    crossFilteredId = models.CharField(max_length=10)
    followTime = models.DateTimeField()
    followBackTime = models.DateTimeField()
        
    def __unicode__(self):
        return self.job
    