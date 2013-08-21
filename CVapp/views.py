from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect,Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from forms import jobForm_step1_subjects, jobForm_step2_crossType, jobForm_step3_params, jobForm_step5_valParams#, jobForm_step4_followUsers  
from models import Job, CrossData
from getFFcount import getFFcount
import getCrossData
from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp, SocialAccount
from twython import Twython, TwythonError, TwythonRateLimitError
import time
import ast
import tasks #delme!!!

MY_KEYS = ['id_str','name','status','statuses_count','screen_name','description','profile_image_url','follow_request_sent','followers_count','friends_count','verified']

def homepage(request):
    if request.user.is_authenticated():
        Jobs = Job.objects.filter(userName=request.user)
        if Jobs:
            currentJob = Jobs[0]
            
            
            if currentJob.jobStep == 1:
                if request.method == 'POST':
                    form = jobForm_step1_subjects(request.POST)
                    if form.is_valid():
                        currentJob.jobStep = 2 
                        currentJob.save()
                        currentJob.subject1Name = request.POST['subject1Name']
                        currentJob.subject2Name = request.POST['subject2Name']                       
                        userFFcount = getFFcount(str(request.user))
                        sub1FFcount = getFFcount(request.POST['subject1Name'])
                        sub2FFcount = getFFcount(request.POST['subject2Name'])
                        # Checking for invalid usernames
                        if not sub1FFcount or not sub2FFcount:
                            if not sub1FFcount and not sub2FFcount:
                                message = 'Both usernames are invalid'                  
                            elif not sub1FFcount:
                                message = 'First username is invalid'                        
                            elif not sub2FFcount:                          
                                message = 'Second username is invalid'
                            currentJob.jobStep = 1 
                            currentJob.save()                                
                            return render_to_response('CVapp/step1_subjects.html',{'form': form,'message': message},context_instance=RequestContext(request))
                            
                        
                        currentJob.userNoFollowers = userFFcount[0]
                        currentJob.userNoFriends = userFFcount[1]
                        currentJob.subject1NoFollowers = sub1FFcount[0]
                        currentJob.subject1NoFriends = sub1FFcount[1]
                        currentJob.subject2NoFollowers = sub2FFcount[0]
                        currentJob.subject2NoFriends = sub2FFcount[1]                            
                        currentJob.save()
                        return redirect('homepage')
                    else:
                        #form = jobForm_step1_subjects()
                        message = "Please correct the user names and try again"
                        return render_to_response('CVapp/step1_subjects.html',{'form': form,'message': message},context_instance=RequestContext(request))
                else:
                    form = jobForm_step1_subjects()
                    return render_to_response('CVapp/step1_subjects.html',{'form': form},context_instance=RequestContext(request))
            # LOADING DATA FOR PAGE 2
            elif currentJob.userNoFollowers == -1 and currentJob.jobStep == 2:
                return render_to_response('CVapp/loading1.html',context_instance=RequestContext(request))
            
            
            elif currentJob.jobStep == 2:
                if request.method == 'POST':
                    form = jobForm_step2_crossType(request.POST)
                    if form.is_valid():
                        currentJob.jobStep = 3  
                        currentJob.save()
                        
                        currentJob.P_crossType = request.POST['P_crossType'] 
                        
                        SocialAccountId = SocialAccount.objects.filter(user_id=request.user.id)[0].id 
                        APP_KEY = SocialApp.objects.filter(name='AndreiiTest')[0].client_id 
                        APP_SECRET = SocialApp.objects.filter(name='AndreiiTest')[0].secret
                        OAUTH_TOKEN = SocialToken.objects.filter(account_id=SocialAccountId)[0].token
                        OAUTH_TOKEN_SECRET = SocialToken.objects.filter(account_id=SocialAccountId)[0].token_secret
                                          

                        ### ***************** Getting Cross Users **************************
                        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
                        
                        sub0FollowersIds = getCrossData.getFollowersIds(twitter,currentJob.userName)
                        currentJob.crossUsersProgress = currentJob.crossUsersProgress + '*'
                        currentJob.save()
                        sub1FollowersIds = getCrossData.getFollowersIds(twitter,currentJob.subject1Name)
                        currentJob.crossUsersProgress = currentJob.crossUsersProgress + '*'
                        currentJob.save()                       
                        sub2FollowersIds = getCrossData.getFollowersIds(twitter,currentJob.subject2Name)
                        currentJob.crossUsersProgress = currentJob.crossUsersProgress + '*'
                        currentJob.save()                       
                        sub0FriendsIds = getCrossData.getFriendsIds(twitter,currentJob.userName)
                        currentJob.crossUsersProgress = currentJob.crossUsersProgress + '*'
                        currentJob.save()
                        sub1FriendsIds = getCrossData.getFriendsIds(twitter,currentJob.subject1Name)
                        currentJob.crossUsersProgress = currentJob.crossUsersProgress + '*'
                        currentJob.save()                        
                        sub2FriendsIds = getCrossData.getFriendsIds(twitter,currentJob.subject2Name)    
                        currentJob.crossUsersProgress = currentJob.crossUsersProgress + '*'
                        currentJob.save()                        
                        
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
                                currentJob.crossUsersProgress = currentJob.crossUsersProgress + '*'
                                currentJob.save()                                
                                rawData = getCrossData.twitterLookupUser(twitter,user_id=', '.join([str(e) for e in followersIds_id_groups[jj]]),include_entities='false')
                                rawData_has_keys = [aJob for aJob in rawData if set(MY_KEYS).issubset(aJob.keys())]
                                rawData_relevant = [{your_key: aJob[your_key] for your_key in MY_KEYS} for aJob in rawData_has_keys]
                                chosenUsers = chosenUsers + rawData_relevant   
                        else:
                            chosenUsers = '0'
                        ### *****************************************************************                     
                        
                        currentJob.crossUsersRelevantData = chosenUsers
                        currentJob.save()
                        return redirect('homepage')
                else:
                    form = jobForm_step2_crossType()
                    FFdata = {}
                    FFdata['subject1Name'] = currentJob.subject1Name
                    FFdata['subject2Name'] = currentJob.subject2Name
                    FFdata['userNoFollowers'] = currentJob.userNoFollowers
                    FFdata['userNoFriends'] = currentJob.userNoFriends
                    FFdata['subject1NoFollowers'] = currentJob.subject1NoFollowers
                    FFdata['subject1NoFriends'] = currentJob.subject1NoFriends
                    FFdata['subject2NoFollowers'] = currentJob.subject2NoFollowers
                    FFdata['subject2NoFriends'] = currentJob.subject2NoFriends 
                    return render_to_response('CVapp/step2_crossType.html',{'form': form,'FFdata': FFdata},context_instance=RequestContext(request))  
            # LOADING DATA FOR PAGE 3
            elif not currentJob.crossUsersRelevantData and currentJob.jobStep == 3:
                log = currentJob.crossUsersProgress
                return render_to_response('CVapp/loading2.html',{'log': log},context_instance=RequestContext(request))
            
            
            elif currentJob.jobStep == 3:
                if request.method == 'POST':
                    form = jobForm_step3_params(request.POST,instance=currentJob)
                    if form.is_valid():
                        currentJob.P_minFollowers = request.POST['P_minFollowers'] 
                        currentJob.P_maxFollowers = request.POST['P_maxFollowers'] 
                        currentJob.P_minFriends = request.POST['P_minFriends'] 
                        currentJob.P_maxFriends = request.POST['P_maxFriends'] 
                        currentJob.P_minFFratio = request.POST['P_minFFratio'] 
                        currentJob.P_maxFFratio = request.POST['P_maxFFratio'] 
                        currentJob.P_minNoTweets = request.POST['P_minNoTweets'] 
                        currentJob.P_maxDays = request.POST['P_maxDays'] 
                        if 'recalculate' in request.POST:
                            currentJob.jobStep = 3
                        else:
                            rawData_relevant = ast.literal_eval(currentJob.crossUsersRelevantData)
                            rawData_filtered = [aJob for aJob in rawData_relevant if (int(aJob['followers_count'])>int(currentJob.P_minFollowers) and 
                                  int(aJob['followers_count'])<int(currentJob.P_maxFollowers) and 
                                  int(aJob['friends_count'])>int(currentJob.P_minFriends) and 
                                  int(aJob['friends_count'])<int(currentJob.P_maxFriends) and                                                                          
                                  (float(aJob['followers_count'])/float(aJob['friends_count']))>float(currentJob.P_minFFratio) and 
                                  (float(aJob['followers_count'])/float(aJob['friends_count']))<float(currentJob.P_maxFFratio) and 
                                  int(aJob['statuses_count'])>int(currentJob.P_minNoTweets) and 
                                  (time.time() - time.mktime(time.strptime(aJob['status']['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))/60.0/60.0/24.0 < int(currentJob.P_maxDays) \
                                  )]
        
                            for crossUser in rawData_filtered:
                                newCrossUser = CrossData(job = currentJob, id_str = crossUser['id_str'], name = crossUser['name'], screenName = crossUser['screen_name'], 
                                                        description = crossUser['description'], imageLink = crossUser['profile_image_url'], 
                                                        statusesCount = crossUser['statuses_count'], followersCount = crossUser['followers_count'], 
                                                        friendsCount = crossUser['friends_count'], toFollow = True)
                                newCrossUser.save()                              
                            currentJob.jobStep = 4
                            currentJob.crossUsersRelevantData = ""   #Free some space from the DB                                          
                        currentJob.save()
                        return redirect('homepage')
                else:
                    form = jobForm_step3_params(instance=currentJob)
                    rawData_relevant = ast.literal_eval(currentJob.crossUsersRelevantData)
                    rawData_filtered = [aJob for aJob in rawData_relevant if (int(aJob['followers_count'])>int(currentJob.P_minFollowers) and 
                          int(aJob['followers_count'])<int(currentJob.P_maxFollowers) and 
                          int(aJob['friends_count'])>int(currentJob.P_minFriends) and 
                          int(aJob['friends_count'])<int(currentJob.P_maxFriends) and                                                                          
                          (float(aJob['followers_count'])/float(aJob['friends_count']))>float(currentJob.P_minFFratio) and 
                          (float(aJob['followers_count'])/float(aJob['friends_count']))<float(currentJob.P_maxFFratio) and 
                          int(aJob['statuses_count'])>int(currentJob.P_minNoTweets) and 
                          (time.time() - time.mktime(time.strptime(aJob['status']['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))/60.0/60.0/24.0 < int(currentJob.P_maxDays) \
                          )]
                   
                    return render_to_response('CVapp/step3_params.html',{'form': form,'crossNum': len(rawData_filtered)},context_instance=RequestContext(request))  
            
            
            elif currentJob.jobStep == 4:
                if request.method == 'POST':
                    FollowUsersList = request.POST.getlist('follow')
                    toDeleteCrossDatas = CrossData.objects.filter(job=currentJob).exclude(id_str__in=FollowUsersList) 
                    for toDeleteCrossData in toDeleteCrossDatas:
                        toDeleteCrossData.delete()
                    currentJob.jobStep = 5                        
                    currentJob.save()
                    return redirect('homepage')
                else:
                    crossUsersData = CrossData.objects.filter(job=currentJob).order_by('followersCount')
                    return render_to_response('CVapp/step4_followUsers.html',{'crossUsersData': crossUsersData},context_instance=RequestContext(request))                 
            
            
            elif currentJob.jobStep == 5:
                if request.method == 'POST':
                    form = jobForm_step5_valParams(request.POST)
                    if form.is_valid():
                        currentJob.P_validationDays = request.POST['P_validationDays'] 
                        currentJob.P_validationThreshold = request.POST['P_validationThreshold']    
                        currentJob.jobStep = 10                        
                        currentJob.save()
                        return redirect('homepage')                
                else:
                    form = jobForm_step5_valParams()     
                    return render_to_response('CVapp/step5_validationParameters.html',{'form': form,'crossNum': CrossData.objects.filter(job_id=currentJob.id).count()}, context_instance=RequestContext(request))  


            elif currentJob.jobStep == 10:
                if request.method == 'POST':
                    toDeleteCrossDatas = CrossData.objects.filter(job=currentJob) 
                    for toDeleteCrossData in toDeleteCrossDatas:
                        toDeleteCrossData.delete()                    
                    currentJob.delete()    
                    return redirect('homepage') 
                else:
                    #tasks.FollowUserById() Delme!!!
                    crossUsersFollowData = CrossData.objects.filter(job=currentJob).exclude(followTime=None).order_by('followTime')                       
                    return render_to_response('CVapp/activeJob.html',{'isJobActive':currentJob.isJobActive ,'validationRatio':currentJob.validationRatio, 'P_validationThreshold':currentJob.P_validationThreshold, 'crossUsersFollowData': crossUsersFollowData},context_instance=RequestContext(request))       
            

            else:
                currentJob.jobStep = 1
                currentJob.save()
                form = jobForm_step1_subjects()
                return render_to_response('CVapp/step1_subjects.html',{'form': form},context_instance=RequestContext(request))                                                 
        else:
            newJob = Job(userName=request.user,jobStep=1)
            newJob.save()
            form = jobForm_step1_subjects()
            return render_to_response('CVapp/step1_subjects.html',{'form': form},context_instance=RequestContext(request))         
    else:        
        return render_to_response('homepage.html',context_instance=RequestContext(request))
