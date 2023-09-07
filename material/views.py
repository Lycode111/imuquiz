from django.shortcuts import render
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from .models import Revision
# Create your views here.

class MaterialView(ListView):
    model = Revision
    template_name = 'revision/teaching_material.html'

# def teaching_material(request):
#     model = Quiz
#     return render(request,'revision/teaching_material.html')

def display_file(request, pk):
    # Get the instance of MyModel with the given primary key
    obj = Revision.objects.get(pk=pk)
    # Return a FileResponse to serve the file
    file_url = obj.file.url

    return render(request, 'revision/view_file.html',{'obj':obj,'file_url': file_url})


