from django.contrib import admin
from db.models import CitizenDetail, ManagerDetail, WorkerDetail

# Register your models here.
admin.site.register(CitizenDetail)
admin.site.register(ManagerDetail)
admin.site.register(WorkerDetail)