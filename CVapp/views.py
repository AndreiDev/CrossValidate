from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect,Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from models import Job, CrossData, logJob, logCrossData
from getUserProfile import getUserProfile
import useTwitterAPI
from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp, SocialAccount
from twython import Twython, TwythonError, TwythonRateLimitError
import time
from datetime import timedelta
import ast
import tasks #delme!!!
from ajax import LOGJob

MY_KEYS = ['id_str','name','status','statuses_count','screen_name','description','profile_image_url','follow_request_sent','followers_count','friends_count','verified']

def homepage(request):
    if request.user.is_authenticated():
        Jobs = Job.objects.filter(userName=request.user)
        if Jobs:
            currentJob = Jobs[0]
            
            if currentJob.jobStep == 1:                
                toDeleteCrossDatas = CrossData.objects.filter(job=currentJob) 
                for toDeleteCrossData in toDeleteCrossDatas:
                    toDeleteCrossData.delete()  
                currentJob.delete()    
                newJob = Job(userName=request.user,jobStep=1)
                newJob.save()   
                LOGJob(newJob)           
                return render_to_response('CVapp/step1_subjects.html',context_instance=RequestContext(request))
                  
            elif currentJob.jobStep == 2:
                crossUsers = CrossData.objects.filter(job=currentJob)
                return render_to_response('CVapp/step2_plans.html',{'NofCrossUsers': len(crossUsers)},context_instance=RequestContext(request))
                                 
            elif currentJob.jobStep == 3:
                if request.method == 'POST':
                    FollowUsersList = request.POST.getlist('follow')
                    toDeleteCrossDatas = CrossData.objects.filter(job=currentJob).exclude(id_str__in=FollowUsersList) 
                    for toDeleteCrossData in toDeleteCrossDatas:
                        toDeleteCrossData.delete()
                    currentJob.jobStep = 10                        
                    currentJob.save()
                    LOGJob(currentJob)
                    tasks.FollowUserById()
                    return redirect('homepage')
                else:
                    crossUsersData = CrossData.objects.filter(job=currentJob).order_by('followersCount')
                    return render_to_response('CVapp/step3_followUsers.html',{'crossUsersData': crossUsersData},context_instance=RequestContext(request))                 
                        
            
            elif currentJob.jobStep == 10:
                if request.method == 'POST':
                    toDeleteCrossDatas = CrossData.objects.filter(job=currentJob) 
                    for toDeleteCrossData in toDeleteCrossDatas:
                        toDeleteCrossData.delete()     
                                   
                    currentJob.delete()    
                    return redirect('homepage') 
                else:
                    crossUsersFollowData = CrossData.objects.filter(job=currentJob).exclude(followTime=None).order_by('followTime')   
                    NFollowed = len(CrossData.objects.filter(job=currentJob).exclude(followTime=None))
                    NFollow = len(CrossData.objects.filter(job=currentJob)) - NFollowed    
                    endOfValidation = str(currentJob.jobDateTime+timedelta(days=int(currentJob.P_validationDays)))[:19]
                    return render_to_response('CVapp/activeJob.html',{'isJobActive':currentJob.isJobActive ,'NFollowed':NFollowed,'NFollow':NFollow,'validationRatio':int(currentJob.validationRatio*100), 'P_validationThreshold':int(currentJob.P_validationThreshold*100),'endOfValidation':endOfValidation, 'crossUsersFollowData': crossUsersFollowData},context_instance=RequestContext(request))       

            else:
                currentJob.jobStep = 1
                currentJob.save()
                
                return render_to_response('CVapp/step1_subjects.html',context_instance=RequestContext(request))                                                 
        else:
            newJob = Job(userName=request.user,jobStep=1)
            newJob.save()
            LOGJob(newJob)
            return render_to_response('CVapp/step1_subjects.html',context_instance=RequestContext(request))         
    else:        
        return render_to_response('homepage.html',context_instance=RequestContext(request))

def plan1(request):
    Jobs = Job.objects.filter(userName=request.user)
    if Jobs:
        currentJob = Jobs[0]                
        toDeleteCrossDatas = CrossData.objects.filter(job=currentJob).order_by('followersCount')[100:]
        for toDeleteCrossData in toDeleteCrossDatas:
            toDeleteCrossData.delete()
        currentJob.plan = 1
        currentJob.jobStep = 3                        
        currentJob.save()
        LOGJob(currentJob)    
    return redirect('homepage')
def plan2(request):
    Jobs = Job.objects.filter(userName=request.user)
    if Jobs:
        currentJob = Jobs[0]      
        currentJob.plan = 2          
        currentJob.jobStep = 3                        
        currentJob.save()
        LOGJob(currentJob)    
    return redirect('homepage')    