from models import Job, CrossData
from celery import task
import time
import getCrossData
from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp, SocialAccount
from twython import Twython, TwythonError, TwythonRateLimitError
from django.contrib.auth.models import User
import datetime
from django.utils.timezone import utc

@task()
def FollowUserById():
    MAX_DAYS_TO_DELETE_JOB = 90
    jobs = Job.objects.all()
        
    for job in jobs:        
        if job.isJobActive == True:
            
            # update validity of job (by P_validationDays timeout) & check if deletion is in order (by MAX_DAYS_TO_DELETE_JOB timeout)
            if (time.time() - time.mktime(time.strptime(str(job.jobDateTime)[:19],'%Y-%m-%d %H:%M:%S')))/60.0/60.0/24.0 > MAX_DAYS_TO_DELETE_JOB:
                toDeleteCrossDatas = CrossData.objects.filter(job=job) 
                for toDeleteCrossData in toDeleteCrossDatas:
                    toDeleteCrossData.delete()                    
                job.delete()  
                continue             
            if (time.time() - time.mktime(time.strptime(str(job.jobDateTime)[:19],'%Y-%m-%d %H:%M:%S')))/60.0/60.0/24.0 > int(job.P_validationDays):
                job.isJobActive = False
                if len(CrossData.objects.filter(job=job).exclude(followTime=None)) == 0:
                    job.validationRatio = 0
                else:
                    job.validationRatio = len(CrossData.objects.filter(job=job).exclude(followBackTime=None))/len(CrossData.objects.filter(job=job).exclude(followTime=None))                        
                job.jobStep = 10 # should be 20 when Unfollowing model is implemented
                job.save()
                continue
        
            # get Friends and Followers IDs    
            userID = User.objects.filter(username=job.userName)[0].id
            SocialAccountId = SocialAccount.objects.filter(user_id=userID)[0].id 
            APP_KEY = SocialApp.objects.filter(name='AndreiiTest')[0].client_id 
            APP_SECRET = SocialApp.objects.filter(name='AndreiiTest')[0].secret
            OAUTH_TOKEN = SocialToken.objects.filter(account_id=SocialAccountId)[0].token
            OAUTH_TOKEN_SECRET = SocialToken.objects.filter(account_id=SocialAccountId)[0].token_secret
                              
            twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)            

            jobFriendsIds = getCrossData.getFriendsIds(twitter,job.userName) 
            jobFollowersIds = getCrossData.getFollowersIds(twitter,job.userName)                                        
            
            # update with new Friends and Followers 
            for crossUser in CrossData.objects.filter(job=job).filter(followTime=None): 
                if int(crossUser.id_str) in jobFriendsIds:
                    crossUser.followTime = datetime.datetime.utcnow().replace(tzinfo=utc)
                    crossUser.toFollow = False
                    crossUser.save()
            for crossUser in CrossData.objects.filter(job=job).filter(followBackTime=None): 
                if int(crossUser.id_str) in jobFollowersIds:
                    crossUser.followBackTime = datetime.datetime.utcnow().replace(tzinfo=utc) 
                    crossUser.save()  
                    
            # Follow a cross-user
            crossUsersToFollow = CrossData.objects.filter(job=job).filter(followTime=None).filter(toFollow=True)
            if not crossUsersToFollow:               
                print "No one to follow" # Done following - waiting for follow-backs till the end of validation period
            else:
                crossUserToFollow = crossUsersToFollow[0]
                try:
                    result = getCrossData.followUser(twitter,crossUserToFollow.screenName)
                except:
                    result = None
                crossUserToFollow.toFollow = False
                if result:
                    crossUserToFollow.followTime = datetime.datetime.utcnow().replace(tzinfo=utc)
                    crossUserToFollow.save()
                else:
                    crossUserToFollow.followTime = None
                    crossUserToFollow.save()
            
            # Update the validationRation
            if len(CrossData.objects.filter(job=job).exclude(followTime=None)) == 0:
                job.validationRatio = 0
            else:
                job.validationRatio = float(len(CrossData.objects.filter(job=job).exclude(followBackTime=None)))/float(len(CrossData.objects.filter(job=job).exclude(followTime=None)))
            job.save()
        else:
            # add Unfollowing algorithm
            continue            