from django.shortcuts import render, redirect
from .models import Quiz
from django.views.generic import ListView
from django.http import JsonResponse
from questions.models import Question,Answer
from results.models import Result,Analysis,UserResult

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import RegisterForm

# Create your views here.
     

def is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'
#?? part 2

class QuizListView(ListView):
    model = Quiz
    template_name = 'quizzes/main.html'

#??? part 2
def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'quizzes/quiz.html',{'obj':quiz})

#assigning the ans and question to a dictionary 
def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    diagrams = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)

        questions.append({str(q): answers})
        if q.question_diagram:
            diagrams.append({str(q): q.question_diagram.url})
        else:
            diagrams.append({str(q): ''})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
        'diagrams': diagrams
    })

def save_quiz_view(request, pk):
    if is_ajax(request):
        questions = []
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')
        for k in data_.keys():
            question = Question.objects.filter(text=k).first()
            explanation_text = Question.objects.filter(text=k).first().explanation_text
            explanation_video = Question.objects.filter(text=k).first().explanation_video
            if question not in questions:
                questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)
        score = 0 
        num_all_questions = quiz.number_of_questions
        multiplier = 100 / quiz.number_of_questions
        results = []
        got_correct_answer=[]
        missed_question = 0
        num_correct_answer = 0
        num_wrong_answer = 0
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)
            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                            num_correct_answer += 1
                            
                    else:
                        if a.correct:
                            correct_answer = a.text
                            num_wrong_answer +=1
                    
                results.append({str(q):{'correct_answer': correct_answer,'answered': a_selected}})
            else:
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a.correct:
                        correct_answer = a.text
                # results.append({str(q): 'not answered'})
                results.append({str(q): {'correct_answer': correct_answer,'answered': 'not answered'}})
                missed_question += 1
        
        score_ = score * multiplier
        Result.objects.create(quiz= quiz.name, user=user, score=score_)

        user_analysis, created = Analysis.objects.get_or_create(user=user, quiz=quiz)
        # Update the existing UserResult object
        user_analysis.total_questions=num_all_questions
        user_analysis.correct_questions=num_correct_answer
        user_analysis.wrong_questions = num_wrong_answer
        user_analysis.skipped_questions= missed_question
        user_analysis.save()


        user_result, created = UserResult.objects.get_or_create(user=user, quiz=quiz)
        # Update the existing UserResult object
        user_result.score = score_
        user_result.required_score = quiz.required_score_to_pass
        user_result.save()

        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({'passed': True, 'score':score_, 'results':results, 'explanation_video':explanation_video, 'explanation_text':explanation_text})
        else:
            return JsonResponse({'passed':False, 'score':score_, 'results':results})



#registration related function views
def register_view(request):
    if request.user.is_authenticated:
        return redirect('quizzes:main-view')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username = username, password = password)
                login(request, user)
                messages.success(request, 'Account was created for ' + username + '!')
                return redirect('quizzes:main-view')
        else:
            form = RegisterForm
            context = {
                'form': form
            }
            return render(request, 'quizzes/register.html', context)

    context = {
        'form': form
    }
    return render(request, 'quizzes/register.html', context)

def login_view(request):
    if 'next' in request.GET:
        messages.info(request, 'You need to be logged in! Please try again!')

    if request.user.is_authenticated:
        return redirect('quizzes:main-view')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)
                messages.success(request, "You have logged in succesfully!")
                return redirect('quizzes:main-view')
            else:
                messages.info(request, 'Username OR password is incorrect!')
                return redirect('quizzes:login')
        else:
            context = {}
            return render(request, 'quizzes/login.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out succesfully!")
    return redirect('quizzes:login')
