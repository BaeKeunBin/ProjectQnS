from django.db import models
from django.utils import timezone
# Create your models here.

class Professor(models.Model):
	email = models.CharField(primary_key = True, max_length = 200, help_text="교수님의 이메일")
	password = models.CharField(max_length=100, default='default', help_text="교수님의 패스워드")
	name = models.CharField(max_length=100, default='default', help_text="교수님의 성함")

	def __str__(self):
		return self.name

class SurveyPost(models.Model):
	postNum = models.AutoField(primary_key = True, help_text="설문조사 번호")
	title = models.CharField(max_length=500, default='default',help_text="설문 조사 명")
	name = models.CharField(max_length=100, default='default',help_text="작성자명")
	subject = models.CharField(max_length=200, default='default',help_text="과목명")
	useTemplate = models.BooleanField(default="True",help_text="기존의 템플릿 사용 여부")

	def __str__(self):
		return self.title

class SurveyQuestion(models.Model):
	post = models.ForeignKey(SurveyPost,on_delete=models.CASCADE)
	QuestionNum = models.IntegerField(default=0,help_text="질문 번호")
	Question = models.CharField(max_length=500, default='default',help_text="질문")

	def __str__(self):
		return self.Question

class Answer(models.Model):
	post = models.ForeignKey(SurveyPost,on_delete=models.CASCADE)
	QuestionNum = models.IntegerField(default=0,help_text="질문 번호")
	studentNum = models.IntegerField(default=0,help_text="학번")
	name = models.CharField(max_length=100, default='default',help_text="학생 이름")
	answer = models.CharField(max_length=1000, default='default',help_text="답변")

	def __str__(self):
		return self.answer

class Student(models.Model):
	studentNum = models.IntegerField(primary_key=True,help_text="학번")
	name = models.CharField(max_length=100, default='default',help_text="학생 이름")
	department = models.CharField(max_length=100, default='default',help_text="학과")

	def __str__(self):
		return self.name

class Subject(models.Model):
	subjectName = models.CharField(max_length=100,help_text="과목이름")
	code = models.CharField(max_length=100,help_text="과목 코드")

	def __str__(self):
		return self.subjectName

class ExtraQ(models.Model):
	subjectName = models.CharField(max_length=100,help_text="과목 이름")
	starRate = models.FloatField(default=0.0,help_text="별점")
	extraQ = models.CharField(max_length=1000, default='default',help_text="추가질문 답변")

	def __str__(self):
		return self.subjectName