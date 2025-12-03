from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.getusers, name='getusers'),
    path('users/adduser/', views.adduser, name='adduser'),
    path('users/edituser/<int:pk>/', views.edituser, name='edituser'),
    path('users/deleteuser/<int:pk>/', views.del_user, name='del_user'),
    path('users/signin/', views.sign_in, name='sign_in'),
    path('users/signup/', views.sign_up, name='sign_up'),
    path('users/signout/', views.sign_out, name='sign_out'),
]