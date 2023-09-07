from django.db import models
from quizzes.models import Quiz
# Create your models here.

class Question(models.Model):
    text = models.CharField(max_length=200)
    #imported from other file
    #CASCADE means When the referenced object is deleted, also delete the objects that have a foreign key pointing to it.
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_diagram = models.ImageField(null=True, blank=True, upload_to="diagram/")
    #models functions
    #can add to quiz to know when is the quiz created
    created = models.DateTimeField(auto_now_add=True)
    explanation_text = models.CharField(max_length=1000, blank=True)
    explanation_video = models.URLField(max_length=200, blank=True)
    
    #return text
    def __str__(self):
        return str(self.text)
    #reverse the relationship
    def get_answers(self):
        return self.answer_set.all() #can use relate name too

class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question =models.ForeignKey(Question,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
                            #the text in the Question class
        return f"question: {self.question.text}, answer:{self.text}, correct: {self.correct}"