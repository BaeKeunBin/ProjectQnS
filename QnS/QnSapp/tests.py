from django.test import TestCase
from QnSapp.models import Professor, SurveyPost
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
		print("#####test message######",len(response.json()))
		print(response.json())
		self.assertEqual(2,len(response.json()['title']))