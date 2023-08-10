from django.contrib import admin
from .models import Question, Answer
# Register your models here.

#so tht when add ques, we can add answer in the same window

#This class is used to represent the Answer model as a tabular inline in the Django admin interface.
#The model attribute specifies that the Answer model should be used for this inline
#inline is a feature that allows you to edit related objects on the same page as the parent object.
#TabularInline is a type of inline in Django that displays related objects in a tabular format. 
class AnswerInline(admin.TabularInline):
    model = Answer

#This class is used to represent the Question model in the Django admin interface.
#The inlines attribute specifies that the AnswerInline class should be used to display related Answer objects on the same page as the Question object.
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer)