from models import Job, CrossData
from celery import task

@task()
def FollowUserById():
    newJob = Job(userName='wow',jobStep=1)
    newJob.save()
    newFollower = CrossData(job = newJob, crossFilteredId = '')
    newFollower.save()