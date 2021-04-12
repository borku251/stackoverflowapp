from django.urls import path,include
from . import views
app_name="main"
urlpatterns = [
    path('',views.index,name="index"),
    path('<int:question_id>/', views.detail, name='detail'),
    path('signup/',views.registration_form,name="registration"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('profile/',views.profile,name="profile"),
    path('count/like/<int:question_id>',views.like,name="like"),
    path('count/dislike/<int:question_id>',views.dislike,name="dislike")
]
