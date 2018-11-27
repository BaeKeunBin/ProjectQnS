from django.shortcuts import render
from django.shortcuts import redirect
from .models import Professor, SurveyPost, SurveyQuestion, Answer, Student, Subject, ExtraQ
from django.views.decorators.csrf import csrf_exempt # csrf 사용 안함
from django.core.exceptions import ObjectDoesNotExist #db 에 데이터 없음 예외
from django.http import HttpResponse

import json
import string

# import logging
# Create your views here.
def loginPage(request):
	if request.method == 'POST': # 학생 은 form 의 POST 로 넘어온다
		inputEmail = request.POST.get('inputEmail') # 이름
		inputPassword = request.POST.get('inputPassword') # 학번	
		Studentinfo = Student(studentNum=inputPassword,name=inputEmail,department="컴퓨터 공학과")
		Studentinfo.save()

		#세션에 저장
		request.session['userName'] = inputEmail
		request.session['studentNumber'] = inputPassword
		request.session['isadmin']='0'
		return redirect('menu') # scene 페이지로 보낸다

	return render(request, 'QnSapp/index.html',{})

def menu(request):
	try :
		username = request.session['userName']
		isadmin = request.session['isadmin']
		# print("세션값",username)
	except KeyError:
		return redirect('errorpage')


	return render(request, 'QnSapp/menu.html',{"username":username,"isadmin" : isadmin})

def startSurvey(request):
	try :
		username = 	request.session['userName']
		# print("세션값",username)
	except KeyError:
		return redirect('errorpage')

	if request.method == 'POST':
		title = request.POST.get('InputTitle') # 설문조사 제목
		subject = request.POST.get('InputSubject') # 과목
		tempCheck = request.POST.get('useTemplate') # 기존 템플릿 사용 여부 (on/None)
		numberOfQuestion = int(request.POST.get('numQ')) # 질문 개수

		# print("title : ",title)
		# print("subject : ",subject)
		# print("tempCheck : ",tempCheck)

		if tempCheck == "on": # 템플릿을 이용할 경우
			post = SurveyPost(title=title,name=username,subject=subject,useTemplate=True) # post 생성
			post.save()
		else:
			post = SurveyPost(title=title,name=username,subject=subject,useTemplate=False) # post 생성
			post.save()

			for i in range(1,numberOfQuestion+1):
				tagname = "inputQ_"+str(i)
				question = request.POST.get(tagname)
				questionSet = SurveyQuestion(post=post,QuestionNum=i,Question=question)
				questionSet.save()
		return redirect('menu')

	return render(request, 'QnSapp/startSurvey.html',{"username":username})

def viewSurvey(request):
	try :
		username = 	request.session['userName']
		# print("세션값",username)
	except KeyError:
		return redirect('errorpage')

	return render(request, 'QnSapp/viewSurvey.html',{"username":username})
	
def answerSurvey(request):
	try :
		username = 	request.session['userName']
		#print("세션값",username)
	except KeyError:
		return redirect('errorpage')
	
	if request.method == "POST":
		surveyPostNum = request.session['surveyPostNum'] # post 번호
		numberOfQuestion = int(request.session['numberOfQuestion']) # 질문의 개수 얻어옴
		studentName = request.session['userName'] # 학생이름
		studentNumber = request.session['studentNumber'] # 학번
		print(surveyPostNum)
		extraQ = request.POST.get('extraQ') # 추가질문
		starRate = request.POST.get('starRate') # 별점

		targetPost = SurveyPost.objects.get(postNum = surveyPostNum) # 해당 설문조사 글

		extratup = ExtraQ(subjectName=targetPost.subject,starRate=starRate,extraQ=extraQ)
		extratup.save()

		for i in range(1,numberOfQuestion+1): # 질문 번호별 답
			print("save answer : ",request.POST.get("answer_"+str(i)))
			# print("hihi3 : ",request.POST.get("answer_"+str(i)))
			answerTup = Answer(post=targetPost,QuestionNum=i,name=studentName,studentNum=studentNumber,answer=request.POST.get("answer_"+str(i)))
			answerTup.save()

		return redirect('menu')

	return render(request, 'QnSapp/answerSurvey.html',{"username":username})

def postlist(request):
	try :
		username = 	request.session['userName']
		#print("세션값",username)
	except KeyError:
		return redirect('errorpage')

	if request.method == 'POST':
		surveyPostNum = request.POST.get('surveyPostNum') #선택된 설문번호 저장
		print(surveyPostNum)
		request.session['surveyPostNum'] = surveyPostNum
		return redirect('answerSurvey')


	return render(request, 'QnSapp/postlist.html',{"username":username})


def errorpage(request):
	return render(request, 'QnSapp/errorpage.html',{})

def review(request):
	try :
		username = 	request.session['userName']
		#print("세션값",username)
	except KeyError:
		return redirect('errorpage')

	return render(request, 'QnSapp/reportSurvey.html',{"username":username})
# 이하 Ajex

@csrf_exempt
# 교수 입장에서의 로그인 시도
def userValidation(request):
	inputEmail = request.POST.get('userID') # 이메일
	inputPassword = request.POST.get('userPW')	# 비밀번호	
	# print("이름 : ",inputEmail)
	# print("패스워드 : ",inputPassword)
	try:
		tup = Professor.objects.get(email=inputEmail)
		# print("교수이름 : ",tup.name)
		request.session['userName']= tup.name # 세션에 이름 추가
		request.session['isadmin']='1'
		context={"result" : "true"}
	except ObjectDoesNotExist:
		context={"result" : "false"}

	return HttpResponse(json.dumps(context),"application/json")

@csrf_exempt
def surveyList(request):
	userName = request.session['userName']
	needData = request.POST.get('needData')

	if needData == "all":
		Qset = SurveyPost.objects.all()
	else:
		Qset = SurveyPost.objects.filter(name=userName)

	postNum=[]
	title=[]
	name=[]
	subject=[]
	for i in Qset:
		if i.name == "master":
			continue;
		title.append(i.title)
		postNum.append(i.postNum)
		name.append(i.name)
		subject.append(i.subject)

	context = {"title":title,"postNum":postNum,"name":name,"subject":subject}
	return HttpResponse(json.dumps(context),"application/json")

@csrf_exempt
def questionList(request):
	surveyPostNum = request.session['surveyPostNum']
	postSet = SurveyPost.objects.get(postNum = surveyPostNum) # 설문지를 가져와 제목 얻기
	title = postSet.title
	
	if postSet.useTemplate == True:
		postSet = SurveyPost.objects.get(name="master")

	QSet = SurveyQuestion.objects.filter(post=postSet) # 설문지를 통해 해당 설문지의 질문들을 가져온다

	QNum = []
	Qcontent = []

	request.session['numberOfQuestion'] = len(QSet)
	# print(len(QSet))
	for i in QSet:
		QNum.append(i.QuestionNum)
		Qcontent.append(i.Question)

	context = {"title":title,"QNum":QNum,"Qcontent":Qcontent}
	return HttpResponse(json.dumps(context),"application/json")

@csrf_exempt
def viewQuestion(request):
	postNumber = request.POST.get('postNumber')
	print("targetPost :",postNumber)
	targetPost = SurveyPost.objects.get(postNum=postNumber) # 템플릿 이용을 판단하기위해 해당 포스트 가져옴

	if targetPost.useTemplate == True: # 템플릿을 이용할 경우 
		targetPost = SurveyPost.objects.get(name='master') # 템플릿 포스트 가져옴
		question = SurveyQuestion.objects.filter(post=targetPost) # 질문 모두 가져옴
	else:								#템플릿 안쓸경우
		question = SurveyQuestion.objects.filter(post=targetPost) # 질문 모두 가져옴

	targetPost = SurveyPost.objects.get(postNum=postNumber) # 해당 포스트 다시 가져옴
	answer = Answer.objects.filter(post=targetPost) # 포스트에 해당하는 답변 모두 가져옴
	
	name = []
	Qnum = []
	ans = []
	Question = []

	
	for i in answer:
		print(i.name)
		name.append(i.name)
		Qnum.append(i.QuestionNum)
		ans.append(i.answer)

	for j in question:
		Question.append(j.Question)

	context ={"name" : name,"ans" : ans,"question" : Question}
	return HttpResponse(json.dumps(context),"application/json")

@csrf_exempt
def subjectList(request):
	tupSubject = ExtraQ.objects.all()
	subjectList = []
	for i in tupSubject:
		subjectList.append(i.subjectName)

	subjectList = list(set(subjectList))
	context = {"subjectList":subjectList}
	return HttpResponse(json.dumps(context),"application/json")

@csrf_exempt
def getSubjectInfo(request):
	targetSubject = request.POST.get('subjectName')
	targetTup = ExtraQ.objects.filter(subjectName=targetSubject)
	starRate =[]
	extraAns =[]
	for i in targetTup:
		starRate.append(i.starRate)
		extraAns.append(i.extraQ)

	context = {"starRate":starRate,"extraAns":extraAns}
	return HttpResponse(json.dumps(context),"application/json")