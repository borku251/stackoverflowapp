from django.db import models

class question(models.Model):
    question_text = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text


class answer(models.Model):
    question = models.ForeignKey(question, on_delete=models.CASCADE)
    answer_text=models.CharField(max_length=500)
    def __str__(self):
        return self.answer_text

class comment(models.Model):
    answer = models.ForeignKey(answer, on_delete=models.CASCADE)
    comments_text = models.CharField(max_length=100)
    def __str__(self):
        return self.comments_text