from django.shortcuts import render,redirect
from .models import Homework,Todo
from .forms import HomeworkForm,TodoForm,DashboardForm,SignupCreationForm
from youtubesearchpython import VideosSearch
from django.views.generic import CreateView
from django.urls import reverse_lazy
import requests 
import wikipedia
# Create your views here.
def home(request):
    return render(request,'home.html')

def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = 'https://www.googleapis.com/books/v1/volumes?q='+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title' : answer['items'][i]['volumeInfo']['title'],
                'subtitle' : answer['items'][i]['volumeInfo'].get('subtitle'),
                'description' : answer['items'][i]['volumeInfo'].get('description'),
                'count' : answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories' : answer['items'][i]['volumeInfo'].get('categories'),
                'rating' : answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail' : answer['items'][i]['volumeInfo'].get('imageLinks'),
                'preview' : answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list
            }
        return render(request,'books.html',context)
    else:
        form = DashboardForm
    context = {
        'form':form
    }
    return render(request,'books.html',context)

def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/'+text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text'],
            audio = answer[0]['phonetics'][0]['audio'],
            definition = answer[0]['meanings'][0]['definitions'][0]['definition'],
            example = answer[0]['meanings'][0]['definitions'][0]['example'],
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms'],
            context = {
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms
            }
        except:
            context = {
                'form':form,
                'input':''
            }
        return render(request,'dictionary.html',context)
    else:
        form = DashboardForm()
    context = {
        'form':form
    }
    return render(request,'dictionary.html',context)
def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homework = Homework(
                user = request.user,
                name = request.POST['name'],
                body = request.POST['body'],
                is_finished = finished
            )
            homework.save()
            return redirect('homework')
    else:
        form = HomeworkForm()
    homeworks = Homework.objects.all()
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False    
    context = {
        'homework_done':homework_done,
        'homeworks':homeworks,
        'form':form
    }
    return render(request,'homework.html',context)

def delete_homework(request,pk):
    Homework.objects.get(pk=pk).delete()
    return redirect('homework')

def todo(request):
    if request.method=='POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user = request.user,
                name = request.POST['name'],
                is_finished = finished
            )
            todos.save()
            return redirect('todo')
    else:
        form = TodoForm()
    todos = Todo.objects.all()
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'todos_done':todos_done,
        'todos':todos,
        'form':form
    }
    return render(request,'todo.html',context)
    
def delete_todo(request,pk):
    Todo.objects.get(pk=pk).delete()
    return redirect('todo')

def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request,'wiki.html',context)
    else:
        form=DashboardForm()
        context = {
          'form':form
        }
    return render(request,'wiki.html',context)

def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit=100)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input':text,
                'title' : i['title'],
                'duration' : i['duration'],
                'thumbnail' : i['thumbnails'][0]['url'],
                'channel' : i['channel']['name'],
                'link' : i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime']
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description']=desc
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list
            }
        return render(request,'youtube.html',context)
    else:
        form = DashboardForm
    context = {
        'form':form
    }
    return render(request,'youtube.html',context)

class SignUpView(CreateView):
    form_class = SignupCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
