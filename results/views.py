
import json
from django.shortcuts import render
from .models import Analysis, UserResult, Result
from quizzes.models import Quiz
def index_bar(request):
    user = request.user
    score = []
    required_score =[]
    quiz = []
    quiz = Quiz.objects.order_by('name').values('name').distinct()
    print(quiz)
    quiz_list = [item['name'] for item in quiz]
    trials = UserResult.objects.filter(user=user)
    for trial in trials:
        score.append(trial.score)
        required_score.append(trial.required_score)
    
    return render(request,'barchart.html',{
        'labels':quiz_list,
        'data': score,
        'compare_data': required_score
    })

def index_pie(request):
    user = request.user
    total_questions = 0
    missed_question = 0
    num_correct_answer = 0
    num_wrong_answer = 0
    trials = Analysis.objects.filter(user=user)
    for trial in trials:
        total_questions += trial.total_questions
        missed_question += trial.skipped_questions
        num_correct_answer += trial.correct_questions
        num_wrong_answer += trial.wrong_questions
    
    data = [num_correct_answer,num_wrong_answer,missed_question]
    labels = ["Corrrect Anwered",'Wrong Answered',"Not answered"]
    return render(request,'piechart.html',{
        'labels':labels,
        'data': data,
    })

def index_line(request):
    user = request.user
    trials = Result.objects.filter(user=user)
    quizzes = Quiz.objects.order_by('name').values('name').distinct()
    print(quizzes)
    quizzes_list = [item['name'] for item in quizzes]
    print(quizzes_list)
    data=[]
    user_trial2 = []
    
    for quiz in quizzes_list:
        num = 1
        score=[0]
        user_trial=[0]
        for trial in trials:
            print(trial.quiz)
            if  trial.quiz == quiz:
                print("hello")
                score.append(trial.score) 
                user_trial.append(num)
                num+=1

        if len(user_trial) > len(user_trial2):
            user_trial2 = user_trial
                
        x = {
            'label': quiz,
            'data' : score
        }
        data.append(x)
        print(data)

    return render(request, 'linegraph.html', 
                  {'data': json.dumps(data),
                   'trial': user_trial2})

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

