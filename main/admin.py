from django.contrib import admin
from. import models

# Register your models here.

class questionadmin(admin.ModelAdmin):
    list_display = ('question_text','pub_date',)
    search_fields = ['question_text']

class ansadmin(admin.ModelAdmin):
    list_display = ('question','answer_text',)

class comadmin(admin.ModelAdmin):
    list_display = ('answer','comments_text',)

admin.site.register(models.question,questionadmin)
admin.site.register(models.answer,ansadmin)
admin.site.register(models.comment,comadmin)