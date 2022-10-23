from tkinter import N
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('category/<str:pk>', views.category, name='category'), 
    path('results', views.results, name='results'), 
    path('high_scores/<str:pk>/', views.view_high_scores, name='view_high_scores'),
    path('inter', views.inter, name='inter'),
    path('admin_panel', views.admin_panel, name='admin_panel'),
    path('delete_question/<str:pk>/', views.delete_question, name='delete_question'),
    path('delete_category/<str:pk>/', views.delete_category, name='delete_category'),
    path('add_to_category/<str:pk>/', views.add_to_category, name='add-to-category'),
    path('edit_question/<str:pk>/', views.edit_question, name='edit_question'),
    path('edit_category/<str:pk>/', views.edit_category, name='edit_category'),
    path('reset/<str:pk>/', views.reset_highscores, name='reset')
]