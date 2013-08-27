from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect,Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from models import Job, CrossData
from getUserProfile import getUserProfile
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
                return render_to_response('CVapp/step1_subjects.html',context_instance=RequestContext(request))
                  
            elif currentJob.jobStep == 2:
                if request.method == 'POST':
                    FollowUsersList = request.POST.getlist('follow')
                    toDeleteCrossDatas = CrossData.objects.filter(job=currentJob).exclude(id_str__in=FollowUsersList) 
                    for toDeleteCrossData in toDeleteCrossDatas:
                        toDeleteCrossData.delete()
                    currentJob.jobStep = 10                        
                    currentJob.save()
                    tasks.FollowUserById()
                    return redirect('homepage')
                else:
                    crossUsersData = CrossData.objects.filter(job=currentJob).order_by('followersCount')
                    return render_to_response('CVapp/step2_followUsers.html',{'crossUsersData': crossUsersData},context_instance=RequestContext(request))                 
            
            
            elif currentJob.jobStep == 10:
                if request.method == 'POST':
                    toDeleteCrossDatas = CrossData.objects.filter(job=currentJob) 
                    for toDeleteCrossData in toDeleteCrossDatas:
                        toDeleteCrossData.delete()                    
                    currentJob.delete()    
                    return redirect('homepage') 
                else:
                    crossUsersFollowData = CrossData.objects.filter(job=currentJob).exclude(followTime=None).order_by('followTime')                       
                    return render_to_response('CVapp/activeJob.html',{'isJobActive':currentJob.isJobActive ,'validationRatio':int(currentJob.validationRatio*100), 'P_validationThreshold':int(currentJob.P_validationThreshold*100), 'crossUsersFollowData': crossUsersFollowData},context_instance=RequestContext(request))       
            

            else:
                currentJob.jobStep = 1
                currentJob.save()
                return render_to_response('CVapp/step1_subjects.html',context_instance=RequestContext(request))                                                 
        else:
            newJob = Job(userName=request.user,jobStep=1)
            newJob.save()
            return render_to_response('CVapp/step1_subjects.html',context_instance=RequestContext(request))         
    else:        
        return render_to_response('homepage.html',context_instance=RequestContext(request))
