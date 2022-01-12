from django.contrib import admin
from .models import Question

admin.site.register(Question)   # question 모델을 admin 사이트에 등록
