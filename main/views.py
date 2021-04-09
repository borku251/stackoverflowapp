from django.shortcuts import render,HttpResponseRedirect
from .models import question,answer,comment
from django.http import Http404
from django.urls import reverse

def index(request):
    if request.method == "POST":
        if request.POST['quest']:
            quests=request.POST['quest']
            reg=question(question_text=quests)
            reg.save()
            return HttpResponseRedirect(reverse('main:index'))

    latest_question_list = question.objects.all
    context = {'list': latest_question_list}
    return render(request, 'main/index.html', context)



def detail(request, question_id):

    #for answer
    if request.method == "POST":
        if request.POST.get('ans'):
            p=request.POST.get('ans')
            anss=answer(question=question.objects.get(id=question_id),answer_text=p)
            anss.save()
            return HttpResponseRedirect(reverse('main:detail', kwargs={'question_id':question_id}))


    #for comment
        if request.POST.get('comment'):
            c_id=request.POST.get('answerid')
            p=request.POST.get('comment')
            com=comment(answer=answer.objects.get(id=c_id),comments_text=p)
            com.save()
            return HttpResponseRedirect(reverse('main:detail', kwargs={'question_id':question_id}))


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
    except que.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'main/detail.html', {'question': que,
                                                'imp':answer_list})



