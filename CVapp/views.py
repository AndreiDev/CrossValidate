from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect,Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from forms import jobForm_step1, jobForm_step2, jobForm_step3
from models import Job, FollowBack
from getFFcount import getFFcount
from getCrossData import getCrossData
from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp, SocialAccount

def homepage(request):
    if request.user.is_authenticated():
        activeJob = Job.objects.filter(userName=request.user)
        if activeJob:
            userRecord = activeJob[0]
            if userRecord.jobStep == 1:
                if request.method == 'POST':
                    form = jobForm_step1(request.POST)
                    if form.is_valid():
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
                        userRecord.jobStep = 2  
                        userRecord.save()
                        return redirect('homepage')
                else:
                    form = jobForm_step1()
                    return render_to_response('CVapp/step1.html',{'form': form},context_instance=RequestContext(request))    
            elif userRecord.jobStep == 2:
                if request.method == 'POST':
                    form = jobForm_step2(request.POST)
                    if form.is_valid():
                        userRecord.P_crossType = request.POST['P_crossType'] 
                        
                        SocialAccountId = SocialAccount.objects.filter(user_id=request.user.id)[0].id 
                        APP_KEY = SocialApp.objects.filter(name='AndreiiTest')[0].client_id 
                        APP_SECRET = SocialApp.objects.filter(name='AndreiiTest')[0].secret
                        OAUTH_TOKEN = SocialToken.objects.filter(account_id=SocialAccountId)[0].token
                        OAUTH_TOKEN_SECRET = SocialToken.objects.filter(account_id=SocialAccountId)[0].token_secret
                                          
                        userRecord.crossUsersRelevantData = str(getCrossData(APP_KEY,APP_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET))                        
                        userRecord.jobStep = 3  
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
            elif userRecord.jobStep == 3:
                if request.method == 'POST':
                    form = jobForm_step3(request.POST)
                    if form.is_valid():
                        #userRecord.P_crossType = request.POST['P_crossType'] 
                        userRecord.jobStep = 4  
                        userRecord.save()
                        return redirect('homepage')
                else:
                    form = jobForm_step3()
                    FFdata = {}
                    #FFdata['subject1Name'] = userRecord.subject1Name
                    #FFdata['subject2Name'] = userRecord.subject2Name
                    #FFdata['userNoFollowers'] = userRecord.userNoFollowers
                    #FFdata['userNoFriends'] = userRecord.userNoFriends
                    #FFdata['subject1NoFollowers'] = userRecord.subject1NoFollowers
                    #FFdata['subject1NoFriends'] = userRecord.subject1NoFriends
                    #FFdata['subject2NoFollowers'] = userRecord.subject2NoFollowers
                    #FFdata['subject2NoFriends'] = userRecord.subject2NoFriends 
                    return render_to_response('CVapp/step3.html',{'form': form,'FFdata': FFdata},context_instance=RequestContext(request))  
            elif userRecord.jobStep == 4:
                return render_to_response('CVapp/step4.html',context_instance=RequestContext(request))  
            elif userRecord.jobStep == 5:
                return render_to_response('CVapp/step5.html',context_instance=RequestContext(request))  
            else:
                userRecord.jobStep = 1
                userRecord.save()
                return render_to_response('CVapp/step1.html',context_instance=RequestContext(request))                                                  
        else:
            newJob = Job(userName=request.user,jobStep=1)
            newJob.save()
            return render_to_response('homepage.html',context_instance=RequestContext(request))         
    else:        
        return render_to_response('homepage.html',context_instance=RequestContext(request))
