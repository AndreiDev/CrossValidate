from django.db import models
from django.core.validators import RegexValidator

class Job(models.Model):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    
    jobDateTime = models.DateTimeField(auto_now_add=True)
    jobStep = models.IntegerField(editable=False)
    plan = models.IntegerField(default=0)
    userName = models.CharField(max_length=15, validators=[alphanumeric])
    subject1Name = models.CharField(max_length=15,default='', validators=[alphanumeric])
    subject2Name = models.CharField(max_length=15,default='', validators=[alphanumeric])   
    userNoFollowing = models.IntegerField(default=-1)
    userNoFollowers = models.IntegerField(default=-1)    
    subject1NoFollowers = models.IntegerField(default=-1)
    subject1NoFollowing = models.IntegerField(default=-1)
    subject2NoFollowing = models.IntegerField(default=-1)
    subject2NoFollowers = models.IntegerField(default=-1)    
    crossUsersProgress = models.IntegerField(default=0) 
    crossUsersRelevantData = models.TextField(max_length=500000,default='',editable=False)
    isJobActive = models.BooleanField(default=True)
    validationRatio = models.FloatField(default=0.0)
    P_crossType = models.IntegerField(default=0)
    P_minFollowers = models.IntegerField(default=100)
    P_maxFollowers = models.IntegerField(default=10000)
    P_minFriends = models.IntegerField(default=100)
    P_maxFriends = models.IntegerField(default=10000) 
    P_minFFratio = models.FloatField(default=1.0)
    P_maxFFratio = models.FloatField(default=100.0)
    P_minNoTweets = models.IntegerField(default=1000) 
    P_maxDays = models.IntegerField(default=3)
    P_validationDays = models.IntegerField(default=5)
    P_validationThreshold = models.FloatField(default=0.5) 
    
    def __unicode__(self):
        return self.userName + ':' + str(self.jobDateTime)
    
class logJob(models.Model):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    
    logDateTime = models.DateTimeField(auto_now_add=True)
    
    jobId = models.IntegerField(default=-1)
    jobDateTime = models.DateTimeField()
    jobStep = models.IntegerField(editable=False)
    plan = models.IntegerField(default=0)
    userName = models.CharField(max_length=15, validators=[alphanumeric])
    subject1Name = models.CharField(max_length=15,default='', validators=[alphanumeric])
    subject2Name = models.CharField(max_length=15,default='', validators=[alphanumeric])   
    userNoFollowing = models.IntegerField(default=-1)
    userNoFollowers = models.IntegerField(default=-1)    
    subject1NoFollowers = models.IntegerField(default=-1)
    subject1NoFollowing = models.IntegerField(default=-1)
    subject2NoFollowing = models.IntegerField(default=-1)
    subject2NoFollowers = models.IntegerField(default=-1)    
    crossUsersProgress = models.IntegerField(default=0) 
    crossUsersRelevantData = models.TextField(max_length=500000,default='',editable=False)
    isJobActive = models.BooleanField(default=True)
    validationRatio = models.FloatField(default=0.0)
    P_crossType = models.IntegerField(default=0)
    P_minFollowers = models.IntegerField(default=100)
    P_maxFollowers = models.IntegerField(default=10000)
    P_minFriends = models.IntegerField(default=100)
    P_maxFriends = models.IntegerField(default=10000) 
    P_minFFratio = models.FloatField(default=1.0)
    P_maxFFratio = models.FloatField(default=100.0)
    P_minNoTweets = models.IntegerField(default=1000) 
    P_maxDays = models.IntegerField(default=3)
    P_validationDays = models.IntegerField(default=5)
    P_validationThreshold = models.FloatField(default=0.5) 
    
    def __unicode__(self):
        return self.userName + ':' + str(self.jobDateTime)    
    
class CrossData(models.Model):
    job = models.ForeignKey(Job)
    id_str = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    screenName = models.CharField(max_length=200)
    description = models.CharField(max_length=400, null=True)
    imageLink = models.CharField(max_length=200, null=True)
    statusesCount = models.IntegerField()
    followersCount = models.IntegerField()
    friendsCount = models.IntegerField()
    toFollow = models.BooleanField(default=True)
    followTime = models.DateTimeField(blank=True, null=True)
    followBackTime = models.DateTimeField(blank=True, null=True)
    toUnfollow = models.BooleanField(default=True)
    unFollowTime = models.DateTimeField(blank=True, null=True)
        
    def __unicode__(self):
        return str(self.job)

class logCrossData(models.Model):
    jobId = models.IntegerField()
    id_str = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    screenName = models.CharField(max_length=200)
    description = models.CharField(max_length=400, null=True)
    imageLink = models.CharField(max_length=200, null=True)
    statusesCount = models.IntegerField()
    followersCount = models.IntegerField()
    friendsCount = models.IntegerField()
    toFollow = models.BooleanField(default=True)
    followTime = models.DateTimeField(blank=True, null=True)
    followBackTime = models.DateTimeField(blank=True, null=True)
    toUnfollow = models.BooleanField(default=True)
    unFollowTime = models.DateTimeField(blank=True, null=True)
        
    def __unicode__(self):
        return str(self.job)    
    