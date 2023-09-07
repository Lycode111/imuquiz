from django.db import models
import random

# Create your models here.
#diff modes
DIFF_CHOICES = (
    ('easy','easy'),
    ('medium','medium'),
    ('hard','hard'),
)
#info related to the quiz
class Quiz(models.Model):
    name = models.CharField(max_length=120)
    topic = models.CharField(max_length=120) 
    number_of_questions = models.IntegerField()
    image = models.URLField(default='')
    time = models.IntegerField(help_text='Duration of the quiz in minutes')
    required_score_to_pass = models.IntegerField(help_text='score in %')
    difficluty = models.CharField(max_length=6, choices=DIFF_CHOICES)
    
    #return the name and topic
    def __str__(self):
        return f"{self.name}-{self.topic}"
    #refer to questions model.py question class
    #reverse the relation
    def get_questions(self):      #first question limited to the number of questions(temporary)
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for user_result in self.quiz_results.all():
            user_result.required_score = self.required_score_to_pass
            user_result.save()

    class Meta:
        verbose_name_plural = 'Quizzes'

    
