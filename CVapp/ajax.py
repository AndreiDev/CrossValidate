from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from models import Job, CrossData
from django.contrib.auth.models import User
from getUserProfile import getUserProfile

from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp, SocialAccount
from twython import Twython, TwythonError, TwythonRateLimitError
import useTwitterAPI
import time
import ast

@dajaxice_register()
def AJRateLimit(request, resources):
    
    SocialAccountId = SocialAccount.objects.filter(user_id=request.user.id)[0].id 
    APP_KEY = SocialApp.objects.filter(name='MVPtest')[0].client_id 
    APP_SECRET = SocialApp.objects.filter(name='MVPtest')[0].secret
    OAUTH_TOKEN = SocialToken.objects.filter(account_id=SocialAccountId)[0].token
    OAUTH_TOKEN_SECRET = SocialToken.objects.filter(account_id=SocialAccountId)[0].token_secret
                      
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    rateLimitString = useTwitterAPI.getRateLimit(twitter,resources)  
    waitSeconds = 0
    if int(rateLimitString['resources']['friends']['/friends/ids']['remaining']) < int(rateLimitString['resources']['friends']['/friends/ids']['limit']):
        waitSeconds = int(rateLimitString['resources']['friends']['/friends/ids']['reset'])-time.time()
    if int(rateLimitString['resources']['followers']['/followers/ids']['remaining']) < int(rateLimitString['resources']['followers']['/followers/ids']['limit']):
        waitSeconds = max(waitSeconds,int(rateLimitString['resources']['followers']['/followers/ids']['reset'])-time.time())
    if int(rateLimitString['resources']['users']['/users/lookup']['remaining']) < int(rateLimitString['resources']['users']['/users/lookup']['limit']):
        waitSeconds = max(waitSeconds,int(rateLimitString['resources']['users']['/users/lookup']['reset'])-time.time())            
    
    return simplejson.dumps({'waitSeconds':waitSeconds})

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
            return simplejson.dumps({'message':"username doesn't exist or blocked",'userFollowing':authUserProfile[3],'userFollowers':authUserProfile[4]})
        else:          
            return simplejson.dumps({'message':"username doesn't exist or blocked"})

MY_KEYS = ['id_str','name','status','statuses_count','screen_name','description','profile_image_url','follow_request_sent','followers_count','friends_count','verified']

@dajaxice_register()        
def AJgetCrossUsers(request,Username1_crossFollowing,Username1_crossFollowers,Username2_crossFollowing,Username2_crossFollowers):
    try:
        curJob = Job.objects.filter(userName=request.user)[0]
        
        SocialAccountId = SocialAccount.objects.filter(user_id=request.user.id)[0].id 
        APP_KEY = SocialApp.objects.filter(name='MVPtest')[0].client_id 
        APP_SECRET = SocialApp.objects.filter(name='MVPtest')[0].secret
        OAUTH_TOKEN = SocialToken.objects.filter(account_id=SocialAccountId)[0].token
        OAUTH_TOKEN_SECRET = SocialToken.objects.filter(account_id=SocialAccountId)[0].token_secret
                          
        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        
        sub0FollowersIds = useTwitterAPI.getFollowersIds(twitter,curJob.userName)
        curJob.crossUsersProgress = 10
        curJob.save()
        sub0FollowingIds = useTwitterAPI.getFollowingIds(twitter,curJob.userName)
        curJob.crossUsersProgress = 20
        curJob.save()    
        
        if Username1_crossFollowing:
            sub1FollowingIds = useTwitterAPI.getFollowingIds(twitter,curJob.subject1Name)
            curJob.crossUsersProgress = 25
            curJob.save()
            
        if Username1_crossFollowers:          
            sub1FollowersIds = useTwitterAPI.getFollowersIds(twitter,curJob.subject1Name)
            curJob.crossUsersProgress = 30
            curJob.save()                       
            
        if Username2_crossFollowing:
            sub2FollowingIds = useTwitterAPI.getFollowingIds(twitter,curJob.subject2Name)    
            curJob.crossUsersProgress = 35
            curJob.save()      
        
        if Username2_crossFollowers:  
            sub2FollowersIds = useTwitterAPI.getFollowersIds(twitter,curJob.subject2Name)
            curJob.crossUsersProgress = 40
            curJob.save()                                                            
        
        if Username1_crossFollowing:
            ids_list = sub1FollowingIds
            if Username1_crossFollowers:
                ids_list = list(set(ids_list).intersection(set(sub1FollowersIds)))
            if Username2_crossFollowing:
                ids_list = list(set(ids_list).intersection(set(sub2FollowingIds)))
            if Username2_crossFollowers:
                ids_list = list(set(ids_list).intersection(set(sub2FollowersIds)))
    
            elif Username1_crossFollowers:
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
                
            progressIncrements = int(60/len(followersIds_id_groups))
            chosenUsers = []
            for jj in range(len(followersIds_id_groups)):
                print jj
                curJob.crossUsersProgress = curJob.crossUsersProgress + progressIncrements
                curJob.save()                                
                rawData = useTwitterAPI.twitterLookupUser(twitter,user_id=', '.join([str(e) for e in followersIds_id_groups[jj]]),include_entities='false')
                rawData_has_keys = [aCrossUser for aCrossUser in rawData if set(MY_KEYS).issubset(aCrossUser.keys())]
                rawData_relevant = [{your_key: aCrossUser[your_key] for your_key in MY_KEYS} for aCrossUser in rawData_has_keys]
                chosenUsers = chosenUsers + rawData_relevant   
        else:
            chosenUsers = '0'         
            return simplejson.dumps({'result':2})           
        
        curJob.crossUsersRelevantData = chosenUsers
        curJob.save()   

        rawData_relevant = chosenUsers
        rawData_filtered = [aCrossUser for aCrossUser in rawData_relevant if (int(aCrossUser['followers_count'])>int(curJob.P_minFollowers) and 
              int(aCrossUser['followers_count'])<int(curJob.P_maxFollowers) and 
              int(aCrossUser['friends_count'])>int(curJob.P_minFriends) and 
              int(aCrossUser['friends_count'])<int(curJob.P_maxFriends) and                                                                          
              (float(aCrossUser['followers_count'])/float(aCrossUser['friends_count']))>float(curJob.P_minFFratio) and 
              (float(aCrossUser['followers_count'])/float(aCrossUser['friends_count']))<float(curJob.P_maxFFratio) and 
              int(aCrossUser['statuses_count'])>int(curJob.P_minNoTweets) and 
              (time.time() - time.mktime(time.strptime(aCrossUser['status']['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))/60.0/60.0/24.0 < int(curJob.P_maxDays) \
              )]                             
        
        return simplejson.dumps({'result':1,'crossNum': len(rawData_filtered),
                                 'P_minFollowers':"{:,}".format(curJob.P_minFollowers),'P_maxFollowers':"{:,}".format(curJob.P_maxFollowers),
                                 'P_minFriends':"{:,}".format(curJob.P_minFriends),'P_maxFriends':"{:,}".format(curJob.P_maxFriends),
                                 'P_minFFratio':curJob.P_minFFratio,'P_maxFFratio':curJob.P_maxFFratio,
                                 'P_minNoTweets':"{:,}".format(curJob.P_minNoTweets),'P_maxDays':"{:,}".format(curJob.P_maxDays),
                                 'P_validationDays':"{:,}".format(curJob.P_validationDays),'P_validationThreshold':curJob.P_validationThreshold})
    except:
        return simplejson.dumps({'result':0})
    
@dajaxice_register() 
def AJgetCrossUsers_progress(request):
    curJob = Job.objects.filter(userName=request.user)[0]
    return simplejson.dumps({'progress':curJob.crossUsersProgress})
    
@dajaxice_register()        
def AJrecalculate(request,Following_Minimum,Following_Maximum,Followers_Minimum,Followers_Maximum,FF_Minimum,FF_Maximum,minNoTweets,maxDays):
    curJob = Job.objects.filter(userName=request.user)[0]
        
    curJob.P_minFollowers = Followers_Minimum.replace(",","")
    curJob.P_maxFollowers = Followers_Maximum.replace(",","")
    curJob.P_minFriends = Following_Minimum.replace(",","")
    curJob.P_maxFriends = Following_Maximum.replace(",","")
    curJob.P_minFFratio = FF_Minimum
    curJob.P_maxFFratio = FF_Maximum
    curJob.P_minNoTweets = minNoTweets.replace(",","")
    curJob.P_maxDays = maxDays                                            
    curJob.save()

    rawData_relevant = ast.literal_eval(curJob.crossUsersRelevantData)
    rawData_filtered = [aCrossUser for aCrossUser in rawData_relevant if (int(aCrossUser['followers_count'])>int(curJob.P_minFollowers) and 
          int(aCrossUser['followers_count'])<int(curJob.P_maxFollowers) and 
          int(aCrossUser['friends_count'])>int(curJob.P_minFriends) and 
          int(aCrossUser['friends_count'])<int(curJob.P_maxFriends) and                                                                          
          (float(aCrossUser['followers_count'])/float(aCrossUser['friends_count']))>float(curJob.P_minFFratio) and 
          (float(aCrossUser['followers_count'])/float(aCrossUser['friends_count']))<float(curJob.P_maxFFratio) and 
          int(aCrossUser['statuses_count'])>int(curJob.P_minNoTweets) and 
          (time.time() - time.mktime(time.strptime(aCrossUser['status']['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))/60.0/60.0/24.0 < int(curJob.P_maxDays) \
          )]                            
    
    return simplejson.dumps({'result':1,'crossNum': len(rawData_filtered)})

@dajaxice_register()        
def AJselectUsers(request,Following_Minimum,Following_Maximum,Followers_Minimum,Followers_Maximum,FF_Minimum,FF_Maximum,minNoTweets,maxDays,validationDays,validationThreshold):

    curJob = Job.objects.filter(userName=request.user)[0]
        
    curJob.P_minFollowers = Followers_Minimum.replace(",","")
    curJob.P_maxFollowers = Followers_Maximum.replace(",","")
    curJob.P_minFriends = Following_Minimum.replace(",","")
    curJob.P_maxFriends = Following_Maximum.replace(",","")
    curJob.P_minFFratio = FF_Minimum
    curJob.P_maxFFratio = FF_Maximum
    curJob.P_minNoTweets = minNoTweets.replace(",","")
    curJob.P_maxDays = maxDays   
    curJob.P_validationDays = validationDays
    curJob.P_validationThreshold = validationThreshold  
    curJob.save()

    rawData_relevant = ast.literal_eval(curJob.crossUsersRelevantData)
    rawData_filtered = [aCrossUser for aCrossUser in rawData_relevant if (int(aCrossUser['followers_count'])>int(curJob.P_minFollowers) and 
          int(aCrossUser['followers_count'])<int(curJob.P_maxFollowers) and 
          int(aCrossUser['friends_count'])>int(curJob.P_minFriends) and 
          int(aCrossUser['friends_count'])<int(curJob.P_maxFriends) and                                                                          
          (float(aCrossUser['followers_count'])/float(aCrossUser['friends_count']))>float(curJob.P_minFFratio) and 
          (float(aCrossUser['followers_count'])/float(aCrossUser['friends_count']))<float(curJob.P_maxFFratio) and 
          int(aCrossUser['statuses_count'])>int(curJob.P_minNoTweets) and 
          (time.time() - time.mktime(time.strptime(aCrossUser['status']['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))/60.0/60.0/24.0 < int(curJob.P_maxDays) \
          )]  
    
    for crossUser in rawData_filtered:
        newCrossUser = CrossData(job = curJob, id_str = crossUser['id_str'], name = crossUser['name'], screenName = crossUser['screen_name'], 
                                description = crossUser['description'], imageLink = crossUser['profile_image_url'], 
                                statusesCount = crossUser['statuses_count'], followersCount = crossUser['followers_count'], 
                                friendsCount = crossUser['friends_count'], toFollow = True)
        newCrossUser.save() 
         
    curJob.jobStep = 2
    curJob.save()
        
    return simplejson.dumps({'result':1})

@dajaxice_register()        
def AJcancel(request):
    Jobs = Job.objects.filter(userName=request.user)
    if Jobs:
        currentJob = Jobs[0]                
        toDeleteCrossDatas = CrossData.objects.filter(job=currentJob) 
        for toDeleteCrossData in toDeleteCrossDatas:
            toDeleteCrossData.delete()  
        currentJob.delete()             
    return simplejson.dumps({'result':1})