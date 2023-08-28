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

class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
     
    # waht is pk?
    # for now only
    def __str__(self):
        return str(self.pk)

class Analysis(models.Model):
    total_questions= models.CharField(max_length=10000)
    correct_questions=models.CharField(max_length=10000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


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

