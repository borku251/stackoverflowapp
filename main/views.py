from django.http import HttpResponse
from django.shortcuts import render
from .models import question,answer,comment
from django.http import Http404

def index(request):
    latest_question_list = question.objects.all
    context = {'list': latest_question_list}
    return render(request, 'main/index.html', context)

def detail(request, question_id):
    comment_list=[]
    answer_list=[]
    try:
        que = question.objects.get(id=question_id) # gives specifed question
        for a in que.answer_set.all(): #returns the list of answers for the question
            k=answer.objects.get(id=a.id) #gets the each answer object to get comments of each answer
            for l in k.comment_set.all(): #returns a list of comments of each answer
                comment_list.append(l)
            answer_list.append((a,comment_list))
            comment_list=[]
            for a,b in answer_list:
                print(a.id)
                print(b)
    except que.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'main/detail.html', {'question': que,
                                                'imp':answer_list})



