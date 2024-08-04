from django.urls import path
from main import views
from main.views import login_view

urlpatterns = [
    path('', views.index, name='index'),
    path('parse', views.task_parse, name='parse'),
    path('login/', login_view, name='login'),
]