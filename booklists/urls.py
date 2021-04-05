from django.urls import path
from booklists import views

app_name = 'booklists'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('user/<str:username>/lists', views.lists_index, name='lists_index'),
    path('user/<str:username>/lists/create', views.lists_create, name='lists_create'),
    path('user/<str:username>/lists/<slug:list_slug>', views.lists_edit, name='lists_edit'),
    path('', views.index, name='index'),
]