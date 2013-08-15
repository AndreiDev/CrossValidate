from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect,Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from forms import jobForm_step1
from models import Job, FollowBack

def homepage(request):
    if request.user.is_authenticated():
        foundUsers = Job.objects.filter(userName=request.user)
        if foundUsers:
            userRecord = foundUsers[0]
            if userRecord.jobStep == 1:
                if request.method == 'POST':
                    form = jobForm_step1(request.POST)
                    if form.is_valid():
                        userRecord.subject1Name = request.POST['subject1Name']
                        userRecord.subject2Name = request.POST['subject2Name']
                        userRecord.jobStep = 2
                        
                        userRecord.save()
                        return redirect('homepage')
                else:
                    form = jobForm_step1()
                    return render_to_response('CVapp/step1.html',{'form': form},context_instance=RequestContext(request))    
            elif userRecord.jobStep == 2:
                return render_to_response('CVapp/step2.html',context_instance=RequestContext(request))  
            elif userRecord.jobStep == 3:
                return render_to_response('CVapp/step3.html',context_instance=RequestContext(request))  
            elif userRecord.jobStep == 4:
                return render_to_response('CVapp/step4.html',context_instance=RequestContext(request))  
            elif userRecord.jobStep == 5:
                return render_to_response('CVapp/step5.html',context_instance=RequestContext(request))  
            else:
                userRecord.jobStep = 1
                userRecord.save()
                return render_to_response('CVapp/step1.html',context_instance=RequestContext(request))                                                  
        else:
            newUser = Job(userName=request.user,jobStep=1)
            newUser.save()
            return render_to_response('homepage.html',context_instance=RequestContext(request))         
    else:        
        return render_to_response('homepage.html',context_instance=RequestContext(request))
