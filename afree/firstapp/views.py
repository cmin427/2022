from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from main_web import afree
from firstapp.models import Document
from firstapp.forms import DocumentForm
from django.template.response import TemplateResponse
from django.template.base import TemplateSyntaxError
# import main_web.py

# Create your views here.
def home(request):
    # uploaded_file_url = None
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'home.html', {'uploaded_file_url': uploaded_file_url})
    # context = {'uploaded_file_url':uploaded_file_url}
    return render(request, 'home.html')

def judge(request):  
    # a = uploaded_file_url  
    # videoname = uploaded_file_url[1:]
    if request.method == 'POST':
        # import main_web
        # os.system('python main_web.py')
        a = request.POST['uploaded_file_url'][1:]
        a1 = a[:-4]
        afree('C:\\Users\\min\\Desktop\\project\\A-free\\web\\firstproject\\'+a)
        os.rename('C:\\Users\\min\\Desktop\\project\\A-free\\web\\firstproject\\'+a1+'_tf_out.mp4', 
        'C:\\Users\\min\\Desktop\\project\\A-free\\web\\firstproject\\firstapp\\static\\image\\'+a1+'_tf_out.mp4')
        
        # afree('C:\\Users\\min\\Desktop\\project\\A-free\\web\\firstproject\\kick.mp4')
        return render(request,'judge.html',{'a':a,'a1':a1})
    return render(request,'judge.html')

def result(request):
    b = request.POST.get('a')
    b1 = 'image/' + b[:-4] + '_tf_out.mp4'
    # video_url = Document.objects.get(description=b)
    context = {'b':b,'b1':b1}
    return render(request,'result.html',context)