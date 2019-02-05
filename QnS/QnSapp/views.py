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

################################ 페이지별 view

#로그인 페이지
def loginPage(request):
	if request.method == 'POST': # 학생 은 form 의 POST 로 넘어온다
		#POST 에서 데이터를 얻는다
		inputEmail = request.POST.get('inputEmail') # 이름
		inputPassword = request.POST.get('inputPassword') # 학번	
		# 학생 정보 저장
		Studentinfo = Student(studentNum=inputPassword,name=inputEmail,department="컴퓨터 공학과")
		Studentinfo.save()

		#세션에 저장
		request.session['userName'] = inputEmail
		request.session['studentNumber'] = inputPassword
		request.session['isadmin']='0' #교수인지 학생인지 구별, 0일경우 학생
		# 메뉴 페이지로 이동
		return redirect('menu') 

	return render(request, 'QnSapp/index.html',{})

#메뉴 페이지
def menu(request):
	try :
		#세션에 데이터가 존재할경우 메뉴 페이지 정상 접근, 없을경우 에러페이지 출력
		# print("세션값",username)
		username = request.session['userName']
		isadmin = request.session['isadmin']
	except KeyError:
		return redirect('errorpage')

	#유저 이름 (교수명 or 학생이름) 과 교수인지 학생인지 구분하는 변수 전달
	return render(request, 'QnSapp/menu.html',{"username":username,"isadmin" : isadmin})

#설문지 작성 (교수님만 가능)
def startSurvey(request):
	try :
		#세션에 데이터가 존재할경우 메뉴 페이지 정상 접근, 없을경우 에러페이지 출력
		username = 	request.session['userName']
		# print("세션값",username)
	except KeyError:
		return redirect('errorpage')

	if request.method == 'POST': # POST 에서 데이터 넘겨받음
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
			# 템플릿을 이용하지 않을것이므로 POST 에서 넘어온 질문들을 저장
			for i in range(1,numberOfQuestion+1):
				tagname = "inputQ_"+str(i)
				question = request.POST.get(tagname)
				questionSet = SurveyQuestion(post=post,QuestionNum=i,Question=question)
				questionSet.save()
		return redirect('menu')

	return render(request, 'QnSapp/startSurvey.html',{"username":username})

#설문조사 결과 보기 페이지 (교수만 이용)
def viewSurvey(request):
	try :
		username = 	request.session['userName']
		# print("세션값",username)
	except KeyError:
		return redirect('errorpage')

	return render(request, 'QnSapp/viewSurvey.html',{"username":username})

# 설문 응답 페이지 (학생 이용)
def answerSurvey(request):
	try :
		#세션에 데이터가 존재할경우 메뉴 페이지 정상 접근, 없을경우 에러페이지 출력
		username = 	request.session['userName']
		#print("세션값",username)
	except KeyError:
		return redirect('errorpage')
	
	if request.method == "POST":
		#세션에서 데이터를 얻어온다
		surveyPostNum = request.session['surveyPostNum'] # post 번호
		numberOfQuestion = int(request.session['numberOfQuestion']) # 질문의 개수 얻어옴
		studentName = request.session['userName'] # 학생이름
		studentNumber = request.session['studentNumber'] # 학번
		# print(surveyPostNum)
		#추가 질문에 대한 응답과 별점을 POST 에서 얻어온다
		extraQ = request.POST.get('extraQ') # 추가질문
		starRate = request.POST.get('starRate') # 별점

		#해당하는 설문 조사를 DB 에서 얻어온다
		targetPost = SurveyPost.objects.get(postNum = surveyPostNum) # 해당 설문조사 글

		#추가질문 및 별점 자장
		extratup = ExtraQ(subjectName=targetPost.subject,starRate=starRate,extraQ=extraQ)
		extratup.save()

		#질문별 응답 DB에 저장
		for i in range(1,numberOfQuestion+1): # 질문 번호별 답
			print("save answer : ",request.POST.get("answer_"+str(i)))
			# print("hihi3 : ",request.POST.get("answer_"+str(i)))
			answerTup = Answer(post=targetPost,QuestionNum=i,name=studentName,studentNum=studentNumber,answer=request.POST.get("answer_"+str(i)))
			answerTup.save()

		# 메뉴 페이지로 이동
		return redirect('menu')

	return render(request, 'QnSapp/answerSurvey.html',{"username":username})

#진행중인 설문조사 목록 (학생 이용)
def postlist(request):
	try :
		#세션에 데이터가 존재할경우 메뉴 페이지 정상 접근, 없을경우 에러페이지 출력
		username = 	request.session['userName']
		#print("세션값",username)
	except KeyError:
		return redirect('errorpage')

	if request.method == 'POST':
		surveyPostNum = request.POST.get('surveyPostNum') #선택된 설문번호
		print(surveyPostNum)
		request.session['surveyPostNum'] = surveyPostNum # 세션에 저장

		#answer survey 페이지에서 계속 동작
		return redirect('answerSurvey')


	return render(request, 'QnSapp/postlist.html',{"username":username})

# 에러 출력 페이지
def errorpage(request):
	return render(request, 'QnSapp/errorpage.html',{})

# 과목별 별점 페이지 
def review(request):
	try :
		#세션에 데이터가 존재할경우 메뉴 페이지 정상 접근, 없을경우 에러페이지 출력
		username = 	request.session['userName']
		#print("세션값",username)
	except KeyError:
		return redirect('errorpage')

	return render(request, 'QnSapp/reportSurvey.html',{"username":username})

##################################### 이하 Ajax

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
		request.session['isadmin']='1' # 교수의 경우 '1'
		context={"result" : "true"} # 로그인 성공시 ture
	except ObjectDoesNotExist:
		context={"result" : "false"} # 로그인 실패시 false

	return HttpResponse(json.dumps(context),"application/json")

@csrf_exempt
#진행중인 설문조사 목록 얻어오기
def surveyList(request):
	userName = request.session['userName']
	needData = request.POST.get('needData')
	# 모든 데이터를 얻어올경우 
	if needData == "all":
		Qset = SurveyPost.objects.all()
	#특정 교수님의 설문만 얻어올 경우
	else:
		Qset = SurveyPost.objects.filter(name=userName)

	postNum=[]
	title=[]
	name=[]
	subject=[]
	# 데이터를 담아서 배열로 전송
	for i in Qset:
		# master 는 템플릿 전용
		if i.name == "master":
			continue;
		title.append(i.title)
		postNum.append(i.postNum)
		name.append(i.name)
		subject.append(i.subject)

	context = {"title":title,"postNum":postNum,"name":name,"subject":subject}
	return HttpResponse(json.dumps(context),"application/json")

@csrf_exempt
#질문 목록 받아오기
def questionList(request):
	surveyPostNum = request.session['surveyPostNum']
	postSet = SurveyPost.objects.get(postNum = surveyPostNum) # 설문지를 가져와 제목 얻기
	title = postSet.title
	
	#템플릿을 사용할 경우 미리 생성해둔 master 의 질문으로 대체
	if postSet.useTemplate == True:
		postSet = SurveyPost.objects.get(name="master")

	QSet = SurveyQuestion.objects.filter(post=postSet) # 설문지를 통해 해당 설문지의 질문들을 가져온다

	QNum = []
	Qcontent = []
	#세션에 질문의 길이 저장
	request.session['numberOfQuestion'] = len(QSet)
	# print(len(QSet))
	#질문 목록을 저장
	for i in QSet:
		QNum.append(i.QuestionNum)
		Qcontent.append(i.Question)

	context = {"title":title,"QNum":QNum,"Qcontent":Qcontent}
	return HttpResponse(json.dumps(context),"application/json")

@csrf_exempt
#질문별 답변을 DB 에서 얻어오기
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

	#데이터를 담아서 전송
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
#과목 목록을 DB 에서 얻어오기
def subjectList(request):
	tupSubject = ExtraQ.objects.all()
	subjectList = []
	for i in tupSubject:
		subjectList.append(i.subjectName)
	#중복을 제거
	subjectList = list(set(subjectList))
	context = {"subjectList":subjectList}
	return HttpResponse(json.dumps(context),"application/json")

@csrf_exempt
#추가질문과 별점을 과목별로 얻어오기
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