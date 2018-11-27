from django.contrib import admin
from .models import Professor,SurveyPost,SurveyQuestion,Answer,Student,Subject, ExtraQ

# Register your models here.
admin.site.register(Professor)
admin.site.register(SurveyPost)
admin.site.register(SurveyQuestion)
admin.site.register(Answer)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(ExtraQ)


