from django.urls import path
from booklists import views

app_name = 'booklists'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('', views.index, name='index'),
]