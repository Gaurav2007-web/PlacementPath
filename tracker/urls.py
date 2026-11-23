from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('task/add/', views.add_task, name='add_task'),
    path('task/toggle/<int:pk>/', views.toggle_task, name='toggle_task'),
    path('task/delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('log/add/', views.add_log, name='add_log'),
    path('question/add/', views.add_question, name='add_question'),
    path('question/toggle/<int:pk>/', views.toggle_question, name='toggle_question'),
    path('question/delete/<int:pk>/', views.delete_question, name='delete_question'),
    path('project/add/', views.add_project, name='add_project'),
    path('application/add/', views.add_application, name='add_application'),
]