from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse
from .models import question,answer,comment,question_comment
from django.http import Http404
from django.urls import reverse
from django.contrib.auth.models import User


def index(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.POST['quest']:
                current_user = request.user
                quests=request.POST['quest']
                des=request.POST['desc']
                reg=question(user=User.objects.get(id=current_user.id),question_text=quests,description=des)
                reg.save()
                return HttpResponseRedirect(reverse('main:index'))
        else:
            return HttpResponseRedirect("/login/")

    latest_question_list = question.objects.all
    context = {'list': latest_question_list}
    return render(request, 'main/index.html', context)


def detail(request, question_id):

    #for question_comment
    if request.POST.get('question_com'):
        if request.user.is_authenticated:
            c_id=request.POST.get('q_id')
            p=request.POST.get('question_com')
            current_user = request.user
            com=question_comment(user=User.objects.get(id=current_user.id),
                        question=question.objects.get(id=question_id),
                        comments_text=p,
                        author_id=current_user.id)
            com.save()
            return HttpResponseRedirect(reverse('main:detail', kwargs={'question_id':question_id}))
        else:
            return HttpResponseRedirect("/login/")

    #for answer
    if request.method == "POST":
        if request.POST.get('ans'):
            if request.user.is_authenticated:
                    p=request.POST.get('ans')
                    current_user = request.user
                    anss=answer(user=User.objects.get(id=current_user.id),
                    question=question.objects.get(id=question_id),
                    answer_text=p,
                    author_id=current_user.id,
                    ques_id=question_id)
                    anss.save()
                    return HttpResponseRedirect(reverse('main:detail', kwargs={'question_id':question_id}))
            else:
                    return HttpResponseRedirect("/login/")


    #for comment
        if request.POST.get('comment'):
            if request.user.is_authenticated:
                    c_id=request.POST.get('answerid')
                    p=request.POST.get('comment')
                    current_user = request.user
                    com=comment(user=User.objects.get(id=current_user.id),
                    answer=answer.objects.get(id=c_id),
                    comments_text=p,
                    author_id=current_user.id)
                    com.save()
                    return HttpResponseRedirect(reverse('main:detail', kwargs={'question_id':question_id}))
            else:
                    return HttpResponseRedirect("/login/")

    comment_list=[]
    answer_list=[]
    question_c=[]
    try:
        que = question.objects.get(id=question_id) # gives specified question
        l=que.answer_set.all()
        proper=l.order_by('-is_verified','-votes')
        for a in proper: #returns the list of answers for the questionnot object
            k=answer.objects.get(id=a.id) #gets the each answer object to get comments of each answer
            name=User.objects.get(id=k.author_id).username #to fetch user name amswer
            for l in k.comment_set.all(): #returns a list of comments of each answer
                    kl=comment.objects.get(id=l.id) #gets the each answer object to get comments of each answer
                    name1=User.objects.get(id=kl.author_id).username #to fetch user name comment
                    comment_list.append((kl,name1))
            answer_list.append((a,name,comment_list))
            comment_list=[]

        for b in que.question_comment_set.all():
            k=question_comment.objects.get(id=b.id)
            name=User.objects.get(id=k.author_id).username #to fetch user name amswer
            question_c.append((k,name))

    except que.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'main/detail.html', {'question': que,
                                                'imp':answer_list,
                                                'ab':question_c})



#from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import signup_form
#signup form
def registration_form(request):
    if not request.user.is_authenticated:
        if request.method =="POST":
            fm=signup_form(request.POST)
            if fm.is_valid():
               fm.save()
               messages.success(request,"Account created successfully")
               return HttpResponseRedirect("/signup/")
        else:
            fm=signup_form()

        return render(request,'main/signup.html',{'form':fm})

    else:
        return HttpResponseRedirect("/profile/")

from django.contrib.auth import login,authenticate
from django.contrib.auth import login as site_login
from django.contrib.auth import logout as site_logout
from django.contrib.auth.forms import AuthenticationForm

def login(request):
        if not request.user.is_authenticated:
            if request.method =="POST":
                fm=AuthenticationForm(request=request,data=request.POST)
                if fm.is_valid():
                   uname=request.POST["username"]
                   upass=request.POST["password"]
                   user=authenticate(username=uname,password=upass)
                   if user is not None:
                      site_login(request,user)
                      messages.success(request,"Logged In successfully")
                      return HttpResponseRedirect("/profile/")
            else:
                fm=AuthenticationForm()

            return render(request,'main/login.html',{'form':fm})
        else:
            return HttpResponseRedirect("/profile/")

def profile(request):
    list=[]
    if request.user.is_authenticated:
        k=User.objects.get(id=request.user.id)
        for m in k.answer_set.all():
             list.append(question.objects.get(id=m.ques_id))
        value=set(list)
        return render(request,'main/profile.html',{'name':request.user,
                                                   'question':k.question_set.all(),
                                                   'answer_que':value,})
    else:
        return HttpResponseRedirect("/login/")

def logout(request):
    if request.user.is_authenticated:
        site_logout(request)
        messages.success(request,"Logged Out successfully")
        return HttpResponseRedirect("/login/")
    else:
        return HttpResponseRedirect("/profile/")

def like(request,question_id):
    if request.user.is_authenticated:
        if request.POST.get('like'):
              answer_id=request.POST['like']
              p=answer.objects.get(id=answer_id)
              p.votes=p.votes+1
              p.save()
              return HttpResponseRedirect(reverse('main:detail', kwargs={'question_id':question_id}))
        p=question.objects.get(id=question_id)
        p.votes=p.votes+1
        p.save()
        return HttpResponseRedirect(reverse('main:detail', kwargs={'question_id':question_id}))
    else:
        return HttpResponseRedirect("/profile/")

def dislike(request,question_id):
    if request.user.is_authenticated:
        if request.POST.get('dislike'):
            answer_id=request.POST['dislike']
            p=answer.objects.get(id=answer_id)
            p.votes=p.votes-1
            p.save()
            return HttpResponseRedirect(reverse('main:detail', kwargs={'question_id':question_id}))

        p=question.objects.get(id=question_id)
        p.votes=p.votes-1
        p.save()
        return HttpResponseRedirect(reverse('main:detail', kwargs={'question_id':question_id}))
    else:
        return HttpResponseRedirect("/profile/")



