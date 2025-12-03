from django.urls import path
from . import views

urlpatterns = [
    path('getusers/', views.getusers, name='get_users'),
    path('adduser/', views.adduser, name='add_user'),
    path('edituser/<int:pk>/', views.edituser, name='edit_user'),
    path('deleteuser/<int:pk>/', views.del_user, name='delete_user'),

    path('signup/', views.sign_up, name='signup'),
    path('signin/', views.sign_in, name='signin'),
    path('signout/', views.sign_out, name='signout'),

    path('forgetpassword/', views.forget_password, name='forget_password'),
    path('resetpassword/', views.reset_password, name='reset_password'),
]