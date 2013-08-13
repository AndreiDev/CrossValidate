from django.db import models

class Interaction(models.Model):
    interactionDateTime = models.DateTimeField()
    userName = models.CharField(max_length=200)
    userFollowersIdsList = models.TextField(max_length=50000)
    userFriendsIdsList = models.TextField(max_length=50000)
    subject1Name = models.CharField(max_length=200)
    subject1FollowersIdsList = models.TextField(max_length=50000)
    subject1FriendsIdsList = models.TextField(max_length=250000)
    subject2Name = models.CharField(max_length=200)
    subject2FollowersIdsList = models.TextField(max_length=50000)
    subject2FriendsIdsList = models.TextField(max_length=250000)    
    crossIds = models.TextField(max_length=5000)
    crossUsersRelevantData = models.TextField(max_length=500000)
    crossUsersFilteredData = models.TextField(max_length=500000)
    
    def __unicode__(self):
        return self.userName + ':' + self.interactionDateTime
    
class FollowBack(models.Model):
    interaction = models.ForeignKey(Interaction)
    crossFilteredId = models.CharField(max_length=10)
    followTime = models.DateTimeField()
    followBackTime = models.DateTimeField()
        
    def __unicode__(self):
        return self.interaction
    
class Parameters(models.Model):
    interaction = models.ForeignKey(Interaction)
    P_crossType = models.IntegerField()
    P_minFollowers = models.IntegerField()
    P_maxFollowers = models.IntegerField()
    P_minFriends = models.IntegerField()
    P_maxFriends = models.IntegerField() 
    P_maxDays = models.IntegerField()
    P_unfollowAfter = models.IntegerField()
    P_testAfter = models.IntegerField()
    P_validationThreshold = models.IntegerField()           
      
    def __unicode__(self):
        return self.interaction
    