from models import Job, FollowBack
from celery import task

@task()
def FollowUserById():
    newJob = Job(userName='wow',jobStep=1)
    newJob.save()
    newFollower = FollowBack(job = newJob, crossFilteredId = '')
    newFollower.save()