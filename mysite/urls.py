from django.contrib import admin
from django.urls import include, path
from mysite import views

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('books/', include('books.urls')),
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
]