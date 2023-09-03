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
from results.views import index_bar, index_pie, index_line

app_name = 'quizzes'

urlpatterns = [
    path('login/', login_view, name = "login"),
    path('logout/', logout_view, name = "logout"),
    path('register/', register_view, name = 'register'),

    path('analysis/resultcomparison', index_bar ,name='index_bar'),
    path('analysis/quizanalysis', index_pie ,name='index_pie'),
    path('analysis/performance', index_line ,name='index_line'),

    #related to the pk in views
    path('<int:pk>/', quiz_view, name='quiz-view'),
    path('<int:pk>/data/', quiz_data_view, name='quiz-data-view'),
    path('<int:pk>/save/', save_quiz_view, name='save-view'),

    #most general urls should be at the bottom
    path('', login_required(QuizListView.as_view(), login_url="quizzes:login"),name='main-view'),
    
]