
import ast
from django.shortcuts import render
from .models import Analysis, UserResult

def index(request):
    user = request.user
    score = []
    required_score =[]
    quiz = []
    trials = UserResult.objects.filter(user=user)
    for trial in trials:
        score.append(trial.score)
        required_score.append(trial.required_score)
        quiz.append(str(trial.quiz))
    
    return render(request,'quiz_view.html',{
        'labels':quiz,
        'data': score,
        'compare_data': required_score
    })

# def index(request):
#     user = request.user
#     analysis_objects = Analysis.objects.all()
#     first_obj = analysis_objects.get(pk=4)
#     total_questions = first_obj.total_questions
#     total_questions_list = ast.literal_eval(total_questions)
#     num_of_people_correct = [0 for z in range(len(total_questions_list))]


#     for analysis in analysis_objects:
#         correct_questions = analysis.correct_questions # get the list of correct questions
#         correct_questions_list = ast.literal_eval(correct_questions)
        
#         for x in correct_questions_list:
#             num_of_question = 0
#             for y in total_questions_list:
#                 if x == y:
#                     num_of_people_correct[num_of_question] += 1
#                 num_of_question +=1
    
#     return render(request,'quiz_view.html',{
#         'labels':total_questions,
#         'data': num_of_people_correct
#     })

