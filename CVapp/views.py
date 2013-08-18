from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect,Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from forms import jobForm_step1, jobForm_step2, jobForm_step3, jobForm_step4
from models import Job, FollowBack
from getFFcount import getFFcount
import getCrossData
from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp, SocialAccount
from twython import Twython, TwythonError, TwythonRateLimitError
import time
import ast

MY_KEYS = ['id_str','name','status','statuses_count','screen_name','description','profile_image_url','follow_request_sent','followers_count','friends_count','verified']

def homepage(request):
    if request.user.is_authenticated():
        activeJob = Job.objects.filter(userName=request.user)
        if activeJob:
            userRecord = activeJob[0]
            
            
            if userRecord.jobStep == 1:
                if request.method == 'POST':
                    form = jobForm_step1(request.POST)
                    if form.is_valid():
                        userRecord.jobStep = 2 
                        userRecord.save()
                        userRecord.subject1Name = request.POST['subject1Name']
                        userRecord.subject2Name = request.POST['subject2Name']                       
                        userFFcount = getFFcount(str(request.user))
                        sub1FFcount = getFFcount(request.POST['subject1Name'])
                        sub2FFcount = getFFcount(request.POST['subject2Name'])
                        userRecord.userNoFollowers = userFFcount[0]
                        userRecord.userNoFriends = userFFcount[1]
                        userRecord.subject1NoFollowers = sub1FFcount[0]
                        userRecord.subject1NoFriends = sub1FFcount[1]
                        userRecord.subject2NoFollowers = sub2FFcount[0]
                        userRecord.subject2NoFriends = sub2FFcount[1]                            
                        userRecord.save()
                        return redirect('homepage')
                else:
                    form = jobForm_step1()
                    return render_to_response('CVapp/step1.html',{'form': form},context_instance=RequestContext(request))
            # LOADING DATA FOR PAGE 2
            elif userRecord.userNoFollowers == -1 and userRecord.jobStep == 2:
                return render_to_response('CVapp/loading1.html',context_instance=RequestContext(request))
            
            
            elif userRecord.jobStep == 2:
                if request.method == 'POST':
                    form = jobForm_step2(request.POST)
                    if form.is_valid():
                        userRecord.jobStep = 3  
                        userRecord.save()
                        
                        userRecord.P_crossType = request.POST['P_crossType'] 
                        
                        SocialAccountId = SocialAccount.objects.filter(user_id=request.user.id)[0].id 
                        APP_KEY = SocialApp.objects.filter(name='AndreiiTest')[0].client_id 
                        APP_SECRET = SocialApp.objects.filter(name='AndreiiTest')[0].secret
                        OAUTH_TOKEN = SocialToken.objects.filter(account_id=SocialAccountId)[0].token
                        OAUTH_TOKEN_SECRET = SocialToken.objects.filter(account_id=SocialAccountId)[0].token_secret
                                          

                        ### ***************** Getting Cross Users **************************
                        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
                        
                        sub0FollowersIds = getCrossData.getFollowersIds(twitter,userRecord.userName)
                        userRecord.crossUsersProgress = userRecord.crossUsersProgress + '*'
                        userRecord.save()
                        sub1FollowersIds = getCrossData.getFollowersIds(twitter,userRecord.subject1Name)
                        userRecord.crossUsersProgress = userRecord.crossUsersProgress + '*'
                        userRecord.save()                       
                        sub2FollowersIds = getCrossData.getFollowersIds(twitter,userRecord.subject2Name)
                        userRecord.crossUsersProgress = userRecord.crossUsersProgress + '*'
                        userRecord.save()                       
                        sub0FriendsIds = getCrossData.getFriendsIds(twitter,userRecord.userName)
                        userRecord.crossUsersProgress = userRecord.crossUsersProgress + '*'
                        userRecord.save()
                        sub1FriendsIds = getCrossData.getFriendsIds(twitter,userRecord.subject1Name)
                        userRecord.crossUsersProgress = userRecord.crossUsersProgress + '*'
                        userRecord.save()                        
                        sub2FriendsIds = getCrossData.getFriendsIds(twitter,userRecord.subject2Name)    
                        userRecord.crossUsersProgress = userRecord.crossUsersProgress + '*'
                        userRecord.save()                        
                        
                        ids_list = list(set(sub1FollowersIds).intersection(set(sub2FollowersIds)).intersection(set(sub1FriendsIds)).intersection(set(sub2FriendsIds)).difference(set(sub0FriendsIds)).difference(set(sub0FollowersIds)))
                        
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
                                userRecord.crossUsersProgress = userRecord.crossUsersProgress + '*'
                                userRecord.save()                                
                                rawData = getCrossData.twitterLookupUser(twitter,user_id=', '.join([str(e) for e in followersIds_id_groups[jj]]),include_entities='false')
                                rawData_has_keys = [userData for userData in rawData if set(MY_KEYS).issubset(userData.keys())]
                                rawData_relevant = [{your_key: userData[your_key] for your_key in MY_KEYS} for userData in rawData_has_keys]
                                chosenUsers = chosenUsers + rawData_relevant   
                        else:
                            chosenUsers = '0'
                        ### *****************************************************************                     
                        
                        userRecord.crossUsersRelevantData = chosenUsers
                        userRecord.save()
                        return redirect('homepage')
                else:
                    form = jobForm_step2()
                    FFdata = {}
                    FFdata['subject1Name'] = userRecord.subject1Name
                    FFdata['subject2Name'] = userRecord.subject2Name
                    FFdata['userNoFollowers'] = userRecord.userNoFollowers
                    FFdata['userNoFriends'] = userRecord.userNoFriends
                    FFdata['subject1NoFollowers'] = userRecord.subject1NoFollowers
                    FFdata['subject1NoFriends'] = userRecord.subject1NoFriends
                    FFdata['subject2NoFollowers'] = userRecord.subject2NoFollowers
                    FFdata['subject2NoFriends'] = userRecord.subject2NoFriends 
                    return render_to_response('CVapp/step2.html',{'form': form,'FFdata': FFdata},context_instance=RequestContext(request))  
            # LOADING DATA FOR PAGE 3
            elif not userRecord.crossUsersRelevantData and userRecord.jobStep == 3:
                log = userRecord.crossUsersProgress
                return render_to_response('CVapp/loading2.html',{'log': log},context_instance=RequestContext(request))
            
            elif userRecord.jobStep == 3:
                if request.method == 'POST':
                    form = jobForm_step3(request.POST,instance=userRecord)
                    if form.is_valid():
                        userRecord.P_minFollowers = request.POST['P_minFollowers'] 
                        userRecord.P_maxFollowers = request.POST['P_maxFollowers'] 
                        userRecord.P_minFriends = request.POST['P_minFriends'] 
                        userRecord.P_maxFriends = request.POST['P_maxFriends'] 
                        userRecord.P_minFFratio = request.POST['P_minFFratio'] 
                        userRecord.P_maxFFratio = request.POST['P_maxFFratio'] 
                        userRecord.P_minNoTweets = request.POST['P_minNoTweets'] 
                        userRecord.P_maxDays = request.POST['P_maxDays'] 
                        if 'recalculate' in request.POST:
                            userRecord.jobStep = 3
                        else:
                            userRecord.jobStep = 4
                        userRecord.save()
                        return redirect('homepage')
                else:
                    form = jobForm_step3(instance=userRecord)
                    rawData_relevant = ast.literal_eval(userRecord.crossUsersRelevantData)
                    rawData_filtered = [userData for userData in rawData_relevant if (userData['followers_count']>userRecord.P_minFollowers and 
                          userData['followers_count']<userRecord.P_maxFollowers and 
                          userData['friends_count']>userRecord.P_minFriends and 
                          userData['friends_count']<userRecord.P_maxFriends and                                                                          
                          (float(userData['followers_count'])/float(userData['friends_count']))>userRecord.P_minFFratio and 
                          (float(userData['followers_count'])/float(userData['friends_count']))<userRecord.P_maxFFratio and 
                          userData['statuses_count']>userRecord.P_minNoTweets and 
                          (time.time() - time.mktime(time.strptime(userData['status']['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))/60.0/60.0/24.0 < userRecord.P_maxDays \
                          )]
                    userRecord.crossUsersFilteredData = rawData_filtered
                    userRecord.save()
                    return render_to_response('CVapp/step3.html',{'form': form,'crossNum': len(userRecord.crossUsersFilteredData)},context_instance=RequestContext(request))  
            elif userRecord.jobStep == 4:
                if request.method == 'POST':
                    form = jobForm_step4(request.POST)
                    if form.is_valid():
                        userRecord.P_unfollowAfter = request.POST['P_unfollowAfter'] 
                        userRecord.P_testAfter = request.POST['P_testAfter'] 
                        userRecord.P_validationThreshold = request.POST['P_validationThreshold']    
                        userRecord.jobStep = 5                        
                        userRecord.save()
                        return redirect('homepage')
                else:
                    form = jobForm_step4()
                    return render_to_response('CVapp/step4.html',{'form': form,'crossNum': len(ast.literal_eval(userRecord.crossUsersFilteredData))},context_instance=RequestContext(request))                 
            elif userRecord.jobStep == 5:
                return render_to_response('CVapp/step5.html',context_instance=RequestContext(request))  
            else:
                userRecord.jobStep = 1
                userRecord.save()
                form = jobForm_step1()
                return render_to_response('CVapp/step1.html',{'form': form},context_instance=RequestContext(request))                                                 
        else:
            newJob = Job(userName=request.user,jobStep=1)
            newJob.save()
            form = jobForm_step1()
            return render_to_response('CVapp/step1.html',{'form': form},context_instance=RequestContext(request))         
    else:        
        return render_to_response('homepage.html',context_instance=RequestContext(request))
