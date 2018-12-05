from django.db import models
from django.utils import timezone
# Create your models here.

class Professor(models.Model):
	email = models.CharField(primary_key = True, max_length = 200)
	password = models.CharField(max_length=100, default='default')
	name = models.CharField(max_length=100, default='default')

	def __str__(self):
		return self.name

class SurveyPost(models.Model):
	postNum = models.AutoField(primary_key = True)
	title = models.CharField(max_length=500, default='default')
	name = models.CharField(max_length=100, default='default')
	subject = models.CharField(max_length=200, default='default')
	useTemplate = models.BooleanField(default="True")

	def __str__(self):
		return self.title

class SurveyQuestion(models.Model):
	post = models.ForeignKey(SurveyPost,on_delete=models.CASCADE)
	QuestionNum = models.IntegerField(default=0)
	Question = models.CharField(max_length=500, default='default')

	def __str__(self):
		return self.Question

class Answer(models.Model):
	post = models.ForeignKey(SurveyPost,on_delete=models.CASCADE)
	QuestionNum = models.IntegerField(default=0)
	studentNum = models.IntegerField(default=0)
	name = models.CharField(max_length=100, default='default')
	answer = models.CharField(max_length=1000, default='default')

	def __str__(self):
		return self.answer

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

class ExtraQ(models.Model):
	subjectName = models.CharField(max_length=100)
	starRate = models.FloatField(default=0.0)
	extraQ = models.CharField(max_length=1000, default='default')

	def __str__(self):
		return self.subjectName