from django.db import models

class Job(models.Model):
    jobDateTime = models.DateTimeField(auto_now_add=True)
    jobStep = models.IntegerField(editable=False)
    userName = models.CharField(max_length=200)
    subject1Name = models.CharField(max_length=200,default='')
    subject2Name = models.CharField(max_length=200,default='')   
    userNoFollowers = models.IntegerField(default=-1)
    userNoFriends = models.IntegerField(default=-1)
    subject1NoFollowers = models.IntegerField(default=-1)
    subject1NoFriends = models.IntegerField(default=-1)
    subject2NoFollowers = models.IntegerField(default=-1)
    subject2NoFriends = models.IntegerField(default=-1)
    crossUsersRelevantData = models.TextField(max_length=500000,default='',editable=False)
    crossUsersFilteredData = models.TextField(max_length=500000,default='',editable=False)
    P_crossType = models.IntegerField(default=0)
    P_minFollowers = models.IntegerField(default=200)
    P_maxFollowers = models.IntegerField(default=30000)
    P_minFriends = models.IntegerField(default=100)
    P_maxFriends = models.IntegerField(default=5000) 
    P_minFFratio = models.FloatField(default=1.0)
    P_maxFFration = models.FloatField(default=100.0)
    P_minNoTweets = models.IntegerField(default=1000) 
    P_maxDays = models.IntegerField(default=3)
    P_unfollowAfter = models.IntegerField(default=10)
    P_testAfter = models.IntegerField(default=5)
    P_validationThreshold = models.FloatField(default=0.5) 
    
    def __unicode__(self):
        return self.userName + ':' + str(self.jobDateTime)
    
class FollowBack(models.Model):
    job = models.ForeignKey(Job)
    crossFilteredId = models.CharField(max_length=10)
    followTime = models.DateTimeField()
    followBackTime = models.DateTimeField()
        
    def __unicode__(self):
        return self.job
    