from django.contrib import admin
from CVapp.models import Job, CrossData, logJob, logCrossData

admin.site.register(Job)
admin.site.register(CrossData)
admin.site.register(logJob)
admin.site.register(logCrossData)
