from django.urls import path
from .views import MaterialView ,display_file

app_name = 'material'

urlpatterns = [
    path('teaching material/', MaterialView.as_view() ,name='teaching_material'),
    path('teaching material/<int:pk>/', display_file, name='file-view'),
]