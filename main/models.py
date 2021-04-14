from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class question(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    votes=models.IntegerField(default=0)
    description=models.CharField(max_length=900)
    def __str__(self):
        return self.question_text


class answer(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(question, on_delete=models.CASCADE)
    answer_text=models.CharField(max_length=500)
    author_id=models.IntegerField()
    ques_id=models.IntegerField()
    votes=models.IntegerField(default=0)
    is_verified=models.IntegerField(default=0)
    def __str__(self):
        return self.answer_text

class comment(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answer = models.ForeignKey(answer, on_delete=models.CASCADE)
    comments_text = models.CharField(max_length=100)
    author_id=models.IntegerField()
    def __str__(self):
        return self.comments_text

class question_comment(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question= models.ForeignKey(question, on_delete=models.CASCADE)
    comments_text = models.CharField(max_length=100)
    author_id=models.IntegerField()
    def __str__(self):
        return self.comments_text