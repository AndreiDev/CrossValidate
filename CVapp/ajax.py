from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from models import Job, CrossData
from django.contrib.auth.models import User
from getUserProfile import getUserProfile

@dajaxice_register()
def AJuserStats(request, username, field):
    curJob = Job.objects.filter(userName=request.user)[0]
    # first fetch will get the data of the authorized user
    if curJob.userNoFollowers == -1:
        authUserProfile = getUserProfile(curJob.userName)
        curJob.userNoFollowers = authUserProfile[4]
        curJob.userNoFriends = authUserProfile[3]
        updatedUserProfile = 1
    else:
        updatedUserProfile = 0
    # if an empty string is passed
    if not username:        
        exec 'curJob.'+field+'Name = ""'
        exec 'curJob.'+field+'NoFollowers = -1'
        exec 'curJob.'+field+'NoFriends = -1'
        curJob.save()
        if updatedUserProfile:
            return simplejson.dumps({'message':'','userFollowing':authUserProfile[3],'userFollowers':authUserProfile[4]})
        else:
            return simplejson.dumps({'message':''})
        
    # maybe add a validation not allowing two identical usernames???
    # user enter his own username
    if username == curJob.userName:
        exec 'curJob.'+field+'Name = ""'
        exec 'curJob.'+field+'NoFollowers = -1'
        exec 'curJob.'+field+'NoFriends = -1'        
        curJob.save()
        if updatedUserProfile:
            return simplejson.dumps({'message':"can't use your own username",'userFollowing':authUserProfile[3],'userFollowers':authUserProfile[4]})
        else:        
            return simplejson.dumps({'message':"can't use your own username"})        
    # get the data of the username
    userProfile = getUserProfile(username)
    # if data is found - user exists
    if userProfile:        
        exec 'curJob.'+field+'Name = username'
        exec 'curJob.'+field+'NoFollowers = '+userProfile[4]
        exec 'curJob.'+field+'NoFriends = '+userProfile[3]        
        curJob.save()
        if updatedUserProfile:
            return simplejson.dumps({'name':userProfile[0], 'pic':userProfile[1], 'tweets':userProfile[2],'following':userProfile[3], 'followers':userProfile[4],'userFollowing':authUserProfile[3],'userFollowers':authUserProfile[4]})
        else:             
            return simplejson.dumps({'name':userProfile[0], 'pic':userProfile[1], 'tweets':userProfile[2],'following':userProfile[3], 'followers':userProfile[4]})
    # if data isn't found - user doesn't exists
    else:
        exec 'curJob.'+field+'Name = ""'
        exec 'curJob.'+field+'NoFollowers = -1'
        exec 'curJob.'+field+'NoFriends = -1'        
        curJob.save()
        if updatedUserProfile:
            return simplejson.dumps({'message':'no such user name','userFollowing':authUserProfile[3],'userFollowers':authUserProfile[4]})
        else:          
            return simplejson.dumps({'message':'no such user name'})