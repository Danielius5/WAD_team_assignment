from django.urls import path
from booklists import views

app_name = 'booklists'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('book/<slug:book_name_slug>/',
    views.show_book, name='show_book'),
    path('', views.index, name='index'),
]