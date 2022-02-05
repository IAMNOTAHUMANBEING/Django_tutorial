from django.urls import path
from django.contrib import admin
from . import views

app_name = 'polls' # {% url %} 사용시 어떤 앱의 url.py를 이용하는지 알려주는 기능

urlpatterns = [
    # 제네릭 뷰, URL 패턴 매칭 위에서 아래로 진행하므로 정의하는 순서 유의
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),

    # # ex: /polls/
    # path('', views.index, name='index'),
    # # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]