from django.test import TestCase
from QnSapp.models import Answer, Professor, SurveyPost, SurveyQuestion
# Create your tests here.
# class SmokeTest(TestCase):
# 	def test_bad_maths(self):
# 		self.assertEuqal(1+1,3)

#교수 입장에서의 로그인 시도
class TestLogin(TestCase):
	#데이터 생성
	def setUp(self):
		self.professor = Professor.objects.create(email='gam5546@gmail.com', password='1234')

    #로그인 성공시
	def test_request_normal_login(self):
		response = self.client.post('/userValidation/', {'userID': self.professor.email, 'userPW': self.professor.password})
        #{'result' : 'true'} 반환
		self.assertEqual(response.json()['result'], 'true')
    #로그인 실패시
	def test_request_fail_login(self):
		response = self.client.post('/userValidation/', {'userID': 'wrong_email', 'userPW': 'wrong_password'})
        #{'result' : 'false'} 반환
		self.assertEqual(response.json()['result'], 'false')

#진행중인 설문조사 목록을 얻어올 수 있는지 테스트
class TestGetSurveyList(TestCase):
	
	def setUp(self):
		#세션에 저장되어있는 데이터를 전달
		self.session = self.client.session
		self.session['userName'] = "김교수"
		self.session.save()
		#임시 데이터 3개 생성
		self.number_of_tuple = 3
		self.post1 = SurveyPost.objects.create(
			title="알고리즘 과목 설문조사",
			name="김교수",
			subject="알고리즘",
			useTemplate="False")
		self.post2 = SurveyPost.objects.create(
			title="자료구조 과목 설문조사",
			name="김교수",
			subject="자료구조",
			useTemplate="False")
		self.post3 = SurveyPost.objects.create(
			title="네트워크 과목 설문조사",
			name="이교수",
			subject="네트워크",
			useTemplate="True")

	#진행중인 모든 설문 목록을 얻어온다
	def test_get_list_all(self):
		#needData 에 'all'일 경우 모든 데이터 얻어온다
		response = self.client.post('/surveyList/',{'needData':'all'})
		#데이터 튜플의 개수 = 3 
		self.assertEqual(self.number_of_tuple,len(response.json()['title']))
		
	#세션에 저장된 데이터로 검색하여 해당 목록만 얻어온다
	def test_get_searched_list(self):
		response = self.client.post('/surveyList/',{'needData':'default'})
		# print("#####test message######",len(response.json()))
		# print(response.json())
		self.assertEqual(2,len(response.json()['title']))

#설문별 질문목록 가져오기
class TestGetQuestionList(TestCase):

	def setUp(self):
		#DB 생성
		#설문지 생성
		self.post1 = SurveyPost.objects.create(
			postNum = 0,
			title="알고리즘 과목 설문조사",
			name="김교수",
			subject="알고리즘",
			useTemplate="False")
		self.post2 = SurveyPost.objects.create(
			postNum = 1,
			title="자료구조 과목 설문조사",
			name="김교수",
			subject="자료구조",
			useTemplate="False")
		self.post3 = SurveyPost.objects.create(
			postNum = 2,
			title="네트워크 과목 설문조사",
			name="이교수",
			subject="네트워크",
			useTemplate="True")
		self.master_post = SurveyPost.objects.create(
			postNum = 3,
			title="master",
			name="master",
			subject="master",
			useTemplate="True")
		#템플릿 사용시 질문 개수
		self.using_template_question_number = 3
		# 설문별 질문 내용
		self.template_question1 = SurveyQuestion.objects.create(
			post = self.master_post,
			QuestionNum =0,
			Question="템플릿 전용 질문 1"
			)
		self.template_question2 = SurveyQuestion.objects.create(
			post = self.master_post,
			QuestionNum =1,
			Question="템플릿 전용 질문 2"
			)
		self.template_question3 = SurveyQuestion.objects.create(
			post = self.master_post,
			QuestionNum =2,
			Question="템플릿 전용 질문 3"
			)

		#템플릿 사용시 질문 개수
		self.not_using_template_question_number = 5
		# 설문별 질문 내용
		self.question1 = SurveyQuestion.objects.create(
			post = self.post2,
			QuestionNum =0,
			Question="설문 1번 전용질문 1"
			)
		self.question2 = SurveyQuestion.objects.create(
			post = self.post2,
			QuestionNum =1,
			Question="설문 1번 전용질문 2"
			)
		self.question3 = SurveyQuestion.objects.create(
			post = self.post2,
			QuestionNum =2,
			Question="설문 1번 전용질문 3"
			)
		self.question4 = SurveyQuestion.objects.create(
			post = self.post2,
			QuestionNum =2,
			Question="설문 1번 전용질문 4"
			)
		self.question5 = SurveyQuestion.objects.create(
			post = self.post2,
			QuestionNum =2,
			Question="설문 1번 전용질문 5"
			)
	# 템플릿을 사용한 질문 가져오기
	def test_get_questionlist_using_template(self):
		#세션 생성 템플릿을 사용하는 설문
		self.session = self.client.session
		self.session['surveyPostNum'] = 2
		self.session.save()

		# print("\n #####start test message######\n")
		# #세션의 모든 내용을 출력
		# for key, value in self.client.session.items():
		#     print('{} => {}'.format(key, value))
		# # print("session : ",self.client.session.exists())
		# print('post number : ',self.post3.postNum)
		# print("\n #####end test message######\n")

		response = self.client.post('/questionList/')
		# print("\n #####start test message######\n")
		# print('post number : ',response.json()['Qcontent'])
		# print("\n #####end test message######\n")
		self.assertEqual(self.using_template_question_number,len(response.json()['Qcontent']))

	# 템플릿을 사용하지 않는 질문 가져오기
	def test_get_questionlist_not_use_template(self):
		#세션 생성 템플릿을 사용하지 않는 설문
		self.session = self.client.session
		self.session['surveyPostNum'] = 1
		self.session.save()

		response = self.client.post('/questionList/')
		self.assertEqual(self.not_using_template_question_number,len(response.json()['Qcontent']))

#해당하는 설문의 질문과 답변 가져오기
class TestViewQuestion(TestCase):

	def setUp(self):
		#설문 생성
		self.post1 = SurveyPost.objects.create(
			postNum = 1,
			title="알고리즘 과목 설문조사",
			name="김교수",
			subject="알고리즘",
			useTemplate="False")
		#설문 1번의 질문
		self.question1 = SurveyQuestion.objects.create(
			post = self.post1,
			QuestionNum =0,
			Question="설문 1번 전용질문 1"
			)
		self.question2 = SurveyQuestion.objects.create(
			post = self.post1,
			QuestionNum =1,
			Question="설문 1번 전용질문 2"
			)
		self.question3 = SurveyQuestion.objects.create(
			post = self.post1,
			QuestionNum =2,
			Question="설문 1번 전용질문 3"
			)
		#해당하는 질문의 답변
		self.ans1 = Answer.objects.create(
			post = self.post1,
			name = "김철수",
			QuestionNum = 0,
			answer = "질문1의 답변"
			)
		self.ans1 = Answer.objects.create(
			post = self.post1,
			name = "김철수",
			QuestionNum = 1,
			answer = "질문2의 답변"
			)
		self.ans1 = Answer.objects.create(
			post = self.post1,
			name = "김철수",
			QuestionNum = 2,
			answer = "질문3의 답변"
			)


	def test_get_answer_set(self):

		response = self.client.post('/viewQuestion/',{'postNumber':'1'})

		print("\n #####start test message######\n")
		print('post number : ',response.json()['name'])
		print('post number : ',response.json()['question'])
		print('post number : ',response.json()['ans'])

		print("\n #####end test message######\n")