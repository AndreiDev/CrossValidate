from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from models import Job, CrossData
from django.contrib.auth.models import User
from getUserProfile import getUserProfile

from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp, SocialAccount
from twython import Twython, TwythonError, TwythonRateLimitError
import getCrossData

@dajaxice_register()
def AJuserStats(request, username, field):
    curJob = Job.objects.filter(userName=request.user)[0]
    # first fetch will get the data of the authorized user
    if curJob.userNoFollowers == -1:
        authUserProfile = getUserProfile(curJob.userName)
        curJob.userNoFollowers = authUserProfile[4]
        curJob.userNoFollowing = authUserProfile[3]
        updatedUserProfile = 1
    else:
        updatedUserProfile = 0
    # if an empty string is passed
    if not username:        
        exec 'curJob.'+field+'Name = ""'
        exec 'curJob.'+field+'NoFollowers = -1'
        exec 'curJob.'+field+'NoFollowing = -1'
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
        exec 'curJob.'+field+'NoFollowing = -1'        
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
        exec 'curJob.'+field+'NoFollowing = '+userProfile[3]        
        curJob.save()
        if updatedUserProfile:
            return simplejson.dumps({'name':userProfile[0], 'pic':userProfile[1], 'tweets':userProfile[2],'following':userProfile[3], 'followers':userProfile[4],'userFollowing':authUserProfile[3],'userFollowers':authUserProfile[4]})
        else:             
            return simplejson.dumps({'name':userProfile[0], 'pic':userProfile[1], 'tweets':userProfile[2],'following':userProfile[3], 'followers':userProfile[4]})
    # if data isn't found - user doesn't exists
    else:
        exec 'curJob.'+field+'Name = ""'
        exec 'curJob.'+field+'NoFollowers = -1'
        exec 'curJob.'+field+'NoFollowing = -1'        
        curJob.save()
        if updatedUserProfile:
            return simplejson.dumps({'message':'no such user name','userFollowing':authUserProfile[3],'userFollowers':authUserProfile[4]})
        else:          
            return simplejson.dumps({'message':'no such user name'})

MY_KEYS = ['id_str','name','status','statuses_count','screen_name','description','profile_image_url','follow_request_sent','followers_count','Following_count','verified']

@dajaxice_register()        
def AJgetCrossUsers(request,Username1_crossFollowing,Username1_crossFollowers,Username2_crossFollowing,Username2_crossFollowers):
    curJob = Job.objects.filter(userName=request.user)[0]
    
    SocialAccountId = SocialAccount.objects.filter(user_id=request.user.id)[0].id 
    APP_KEY = SocialApp.objects.filter(name='AndreiiTest')[0].client_id 
    APP_SECRET = SocialApp.objects.filter(name='AndreiiTest')[0].secret
    OAUTH_TOKEN = SocialToken.objects.filter(account_id=SocialAccountId)[0].token
    OAUTH_TOKEN_SECRET = SocialToken.objects.filter(account_id=SocialAccountId)[0].token_secret
                      

    ### ***************** Getting Cross Users **************************
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    sub0FollowersIds = getCrossData.getFollowersIds(twitter,curJob.userName)
    curJob.crossUsersProgress = curJob.crossUsersProgress + '*'
    curJob.save()
    sub0FollowingIds = getCrossData.getFollowingIds(twitter,curJob.userName)
    curJob.crossUsersProgress = curJob.crossUsersProgress + '*'
    curJob.save()    
    
    if Username1_crossFollowing:
        sub1FollowingIds = getCrossData.getFollowingIds(twitter,curJob.subject1Name)
        curJob.crossUsersProgress = curJob.crossUsersProgress + '*'
        curJob.save()
        
    if Username1_crossFollowers:          
        sub1FollowersIds = getCrossData.getFollowersIds(twitter,curJob.subject1Name)
        curJob.crossUsersProgress = curJob.crossUsersProgress + '*'
        curJob.save()                       
        
    if Username2_crossFollowing:
        sub2FollowingIds = getCrossData.getFollowingIds(twitter,curJob.subject2Name)    
        curJob.crossUsersProgress = curJob.crossUsersProgress + '*'
        curJob.save()      
    
    if Username2_crossFollowers:  
        sub2FollowersIds = getCrossData.getFollowersIds(twitter,curJob.subject2Name)
        curJob.crossUsersProgress = curJob.crossUsersProgress + '*'
        curJob.save()                                                            
    
    if Username1_crossFollowing:
        ids_list = sub1FollowingIds
        if Username1_crossFollowers:
            ids_list = list(set(ids_list).intersection(set(sub1FollowersIds)))
        if Username2_crossFollowing:
            ids_list = list(set(ids_list).intersection(set(sub2FollowingIds)))
        if Username2_crossFollowers:
            ids_list = list(set(ids_list).intersection(set(sub2FollowersIds)))

    if Username1_crossFollowers:
        ids_list = sub1FollowersIds
        if Username1_crossFollowing:
            ids_list = list(set(ids_list).intersection(set(sub1FollowingIds)))
        if Username2_crossFollowing:
            ids_list = list(set(ids_list).intersection(set(sub2FollowingIds)))
        if Username2_crossFollowers:
            ids_list = list(set(ids_list).intersection(set(sub2FollowersIds)))           
                                        
    ids_list = list(set(ids_list).difference(set(sub0FollowingIds)).difference(set(sub0FollowersIds)))
    
    ii = 0
    followersIds_GROUP_SIZE = 100
    followersIds_id_groups = []
    
    if ids_list:
        while ii < len(ids_list):
            followersIds_id_groups.append(ids_list[ii:min(ii + followersIds_GROUP_SIZE,len(ids_list))])
            ii = ii + followersIds_GROUP_SIZE    
    
        chosenUsers = []
        for jj in range(len(followersIds_id_groups)):
            print jj
            curJob.crossUsersProgress = curJob.crossUsersProgress + '*'
            curJob.save()                                
            rawData = getCrossData.twitterLookupUser(twitter,user_id=', '.join([str(e) for e in followersIds_id_groups[jj]]),include_entities='false')
            rawData_has_keys = [aJob for aJob in rawData if set(MY_KEYS).issubset(aJob.keys())]
            rawData_relevant = [{your_key: aJob[your_key] for your_key in MY_KEYS} for aJob in rawData_has_keys]
            chosenUsers = chosenUsers + rawData_relevant   
    else:
        chosenUsers = '0'
    ### *****************************************************************                     
    
    curJob.crossUsersRelevantData = chosenUsers
    curJob.save()   
    return simplejson.dumps({'result':1}) 