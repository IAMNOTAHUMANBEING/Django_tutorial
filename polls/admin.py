from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

# 필드가 여러개일 땐 분할 할 수 있음
# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['question_text']}),
#         ('Date information', {'fields': ['pub_date']}),
#     ]

admin.site.register(Question, QuestionAdmin)   # question 모델을 admin 사이트에 등록
# admin.site.register(Choice) 선택지를 각각 등록해서 질문과 연결하는 것보다 질문을 생성할 때 선택지를 생성하는게 효율적

