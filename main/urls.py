from django.urls import path
from main import views
from main.views import login_view

urlpatterns = [
    path('', views.index, name='index'),
    path('parse', views.task_parse, name='parse'),
    path('login/', login_view, name='login'),
    path('download_report/<int:file_id>/', views.download_report, name='download_report'),
    path('create_report/<int:direction_id>/', views.create_report, name='create_report'),
]