from django.db import models
from django.utils import timezone
# Create your models here.

class Professor(models.Model):
	email = models.CharField(primary_key = True, max_length = 200)
	password = models.CharField(max_length=100, default='default')
	name = models.CharField(max_length=100, default='default')

	def __str__(self):
		return self.Name

class SurveyPost(models.Model):
	postNum = models.AutoField(primary_key = True)
	title = models.CharField(max_length=500, default='default')
	name = models.CharField(max_length=100, default='default')
	subject = models.CharField(max_length=200, default='default')

	def __str__(self):
		return self.title

class SurveyQuestion(models.Model):
	postNum = models.ForeignKey(SurveyPost,on_delete=models.CASCADE)
	QuestionNum = models.IntegerField(default=0)
	Question = models.CharField(max_length=500, default='default')

	def __str__(self):
		return self.Question

class Answer(models.Model):
	postNum = models.ForeignKey(SurveyPost,on_delete=models.CASCADE)
	QuestionNum = models.IntegerField(default=0)
	studentNum = models.IntegerField(default=0)
	answer = models.CharField(max_length=1000, default='default')

	def __str__(self):
		return self.QuestionNum

class Student(models.Model):
	studentNum = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=100, default='default')
	department = models.CharField(max_length=100, default='default')

	def __str__(self):
		return self.name

class Subject(models.Model):
	subjectName = models.CharField(max_length=100)
	code = models.CharField(max_length=100)

	def __str__(self):
		return self.subjectName