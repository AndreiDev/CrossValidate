from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from models import Job, CrossData
from django.contrib.auth.models import User
from getUserProfile import getUserProfile

from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp, SocialAccount
from twython import Twython, TwythonError, TwythonRateLimitError
import getCrossData
import time

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

MY_KEYS = ['id_str','name','status','statuses_count','screen_name','description','profile_image_url','follow_request_sent','followers_count','friends_count','verified']

@dajaxice_register()        
def AJgetCrossUsers(request,Username1_crossFollowing,Username1_crossFollowers,Username2_crossFollowing,Username2_crossFollowers):
    try:
        curJob = Job.objects.filter(userName=request.user)[0]
        
        SocialAccountId = SocialAccount.objects.filter(user_id=request.user.id)[0].id 
        APP_KEY = SocialApp.objects.filter(name='AndreiiTest')[0].client_id 
        APP_SECRET = SocialApp.objects.filter(name='AndreiiTest')[0].secret
        OAUTH_TOKEN = SocialToken.objects.filter(account_id=SocialAccountId)[0].token
        OAUTH_TOKEN_SECRET = SocialToken.objects.filter(account_id=SocialAccountId)[0].token_secret
                          
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
        
        curJob.crossUsersRelevantData = chosenUsers
        curJob.save()   
                
        rawData_relevant = chosenUsers
        rawData_filtered = [aJob for aJob in rawData_relevant if (int(aJob['followers_count'])>int(curJob.P_minFollowers) and 
              int(aJob['followers_count'])<int(curJob.P_maxFollowers) and 
              int(aJob['friends_count'])>int(curJob.P_minFriends) and 
              int(aJob['friends_count'])<int(curJob.P_maxFriends) and                                                                          
              (float(aJob['followers_count'])/float(aJob['friends_count']))>float(curJob.P_minFFratio) and 
              (float(aJob['followers_count'])/float(aJob['friends_count']))<float(curJob.P_maxFFratio) and 
              int(aJob['statuses_count'])>int(curJob.P_minNoTweets) and 
              (time.time() - time.mktime(time.strptime(aJob['status']['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))/60.0/60.0/24.0 < int(curJob.P_maxDays) \
              )]                             
        
        return simplejson.dumps({'result':1,'crossNum': len(rawData_filtered),
                                 'P_minFollowers':"{:,}".format(curJob.P_minFollowers),'P_maxFollowers':"{:,}".format(curJob.P_maxFollowers),
                                 'P_minFriends':"{:,}".format(curJob.P_minFriends),'P_maxFriends':"{:,}".format(curJob.P_maxFriends),
                                 'P_minFFratio':"{:,}".format(curJob.P_minFFratio),'P_maxFFratio':"{:,}".format(curJob.P_maxFFratio),
                                 'P_minNoTweets':"{:,}".format(curJob.P_minNoTweets),'P_maxDays':"{:,}".format(curJob.P_maxDays),
                                 'P_validationDays':"{:,}".format(curJob.P_validationDays),'P_validationThreshold':"{:,}".format(curJob.P_validationThreshold)})
    except:
        return simplejson.dumps({'result':0})
    
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
    rawData_filtered = [aJob for aJob in rawData_relevant if (int(aJob['followers_count'])>int(curJob.P_minFollowers) and 
          int(aJob['followers_count'])<int(curJob.P_maxFollowers) and 
          int(aJob['friends_count'])>int(curJob.P_minFriends) and 
          int(aJob['friends_count'])<int(curJob.P_maxFriends) and                                                                          
          (float(aJob['followers_count'])/float(aJob['friends_count']))>float(curJob.P_minFFratio) and 
          (float(aJob['followers_count'])/float(aJob['friends_count']))<float(curJob.P_maxFFratio) and 
          int(aJob['statuses_count'])>int(curJob.P_minNoTweets) and 
          (time.time() - time.mktime(time.strptime(aJob['status']['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))/60.0/60.0/24.0 < int(curJob.P_maxDays) \
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

    rawData_relevant = curJob.crossUsersRelevantData
    rawData_filtered = [aJob for aJob in rawData_relevant if (int(aJob['followers_count'])>int(curJob.P_minFollowers) and 
          int(aJob['followers_count'])<int(curJob.P_maxFollowers) and 
          int(aJob['friends_count'])>int(curJob.P_minFriends) and 
          int(aJob['friends_count'])<int(curJob.P_maxFriends) and                                                                          
          (float(aJob['followers_count'])/float(aJob['friends_count']))>float(curJob.P_minFFratio) and 
          (float(aJob['followers_count'])/float(aJob['friends_count']))<float(curJob.P_maxFFratio) and 
          int(aJob['statuses_count'])>int(curJob.P_minNoTweets) and 
          (time.time() - time.mktime(time.strptime(aJob['status']['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))/60.0/60.0/24.0 < int(curJob.P_maxDays) \
          )]  
    
    for crossUser in rawData_filtered:
        newCrossUser = CrossData(job = curJob, id_str = crossUser['id_str'], name = crossUser['name'], screenName = crossUser['screen_name'], 
                                description = crossUser['description'], imageLink = crossUser['profile_image_url'], 
                                statusesCount = crossUser['statuses_count'], followersCount = crossUser['followers_count'], 
                                friendsCount = crossUser['friends_count'], toFollow = True)
        newCrossUser.save()  
        
    return simplejson.dumps({'result':1})