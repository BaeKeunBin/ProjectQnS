from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns=[
	path('', views.loginPage, name='loginPage'),
	path('menu/', views.menu, name='menu'),
	path('startSurvey/', views.startSurvey, name='startSurvey'),
	path('viewSurvey/', views.viewSurvey, name='viewSurvey'),
	path('answerSurvey/', views.answerSurvey, name='answerSurvey'),
	path('surveyList/',views.surveyList, name="surveyList"),
	path('postlist/',views.postlist,name="postlist"),
	path('review/',views.review,name="review"),

	#errorpage
	path('404error/',views.errorpage,name="errorpage"),
	#ajax url
	path('userValidation/',views.userValidation,name="userValidation"),
	path('questionList/',views.questionList,name="questionList"),
	path('viewQuestion/',views.viewQuestion,name="viewQuestion"),
	path('subjectList/',views.subjectList, name="subjectList"),
	path('getSubjectInfo/',views.getSubjectInfo,name="getSubjectInfo")
]