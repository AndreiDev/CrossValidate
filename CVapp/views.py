from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect,Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from forms import jobCreateForm
from models import Interaction, FollowBack, Parameters

@login_required()
def job_create(request):
    """
    This view handles job creation
    """

    # if the form was submitted via post, process it ie submitted
    if request.method=="POST":
        form = jobCreateForm(request.POST,request.FILES)

        if form.is_valid():
            share = form.save(commit=False)
            share.user = request.user
            share.save()
            return HttpResponseRedirect('/')
        else:
            context     = {'form':form}
            return render_to_response('add_content.html',context,context_instance=RequestContext(request))
    else: 
        form = jobCreateForm()
        return render_to_response('CVapp/job_create.html',{'form': form},context_instance=RequestContext(request))