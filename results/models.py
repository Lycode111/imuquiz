from django.db import models
from quizzes.models import Quiz
from django.contrib.auth.models import User
#new
from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from questions.models import Question, Answer
from django.db import models
import json
import ast
from django.shortcuts import render
# Create your models here.
DEFAULT_VALUE = 1000
class Result(models.Model):
    quiz = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
     
    # for now only
    def __str__(self):
        return str(self.pk)

class Analysis(models.Model):
    total_questions= models.IntegerField(default=DEFAULT_VALUE)
    skipped_questions = models.IntegerField(default=DEFAULT_VALUE)
    correct_questions=models.IntegerField(default=DEFAULT_VALUE)
    wrong_questions=models.IntegerField(default=DEFAULT_VALUE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

class UserResult(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE,  related_name='quiz_results')
    user = models.CharField(max_length=10000)
    score = models.FloatField(default=DEFAULT_VALUE)
    required_score = models.FloatField(default=DEFAULT_VALUE)
     


# class Analysis(models.Model):
#     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     questions = models.ForeignKey(Question, on_delete=models.CASCADE)
#     score = models.FloatField()
#     change_list_template = 'admin/quiz_change_list.html'

#     def get_urls(self):
#         urls = super().get_urls()
#         my_urls = [
#             path('analysis/', self.analysis_view, name='quiz-analysis'),
#         ]
#         return my_urls + urls

#     def analysis_view(self, request, object_id):
#         # Get the quiz object
#         result = Result.objects.get(pk=object_id)
#         quiz = result.quiz
#         quizquestions = quiz.number_of_questions
#         # Get the data you want to analyze
#         data = {"x":3 , "y":4}
#         # Process the data and generate the analysis
#         analysis = data*3

#         context = dict(
#             self.admin_site.each_context(request),
#             analysis=analysis,
#         )
#         return TemplateResponse(request, 'admin/quiz_analysis.html', context)

