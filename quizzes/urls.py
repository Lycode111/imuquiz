from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    QuizListView,
    quiz_view,
    quiz_data_view,
    save_quiz_view,
    login_view,
    logout_view,
    register_view,
)
from results.views import index 

app_name = 'quizzes'

urlpatterns = [
    path('login/', login_view, name = "login"),
    path('logout/', logout_view, name = "logout"),
    path('register/', register_view, name = 'register'),

    path('analysis/', index ,name='index'),

    #related to the pk in views
    path('<pk>/', quiz_view, name='quiz-view'),
    path('<pk>/data/', quiz_data_view, name='quiz-data-view'),
    path('<pk>/save/', save_quiz_view, name='save-view'),

    #most general urls should be at the bottom
    path('', login_required(QuizListView.as_view(), login_url="quizzes:login"),name='main-view'),
    
]