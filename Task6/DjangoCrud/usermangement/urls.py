from django.urls import path
from . import views

urlpatterns = [
    # Admin APIs
    path('getusers/', views.getusers, name='get_users'),
    path('adduser/', views.adduser, name='add_user'),
    path('edituser/<int:pk>/', views.edituser, name='edit_user'),
    path('deleteuser/<int:pk>/', views.del_user, name='delete_user'),
    path('updatepassword/<int:pk>/', views.update_password, name='update_password'),

    # Authentication APIs
    path('signup/', views.sign_up, name='signup'),
    path('verifyemail/', views.verify_email, name='verify_email'),
    path('signin/', views.sign_in, name='signin'),
    path('signout/', views.sign_out, name='signout'),

    # User Profile APIs
    path('viewprofile/', views.view_profile, name='view_profile'),
    path('editprofile/', views.edit_profile, name='edit_profile'),

    # Password Management APIs
    path('changepassword/', views.change_password, name='change_password'),
    path('forgetpassword/', views.forget_password, name='forget_password'),
    path('resetpassword/', views.reset_password, name='reset_password'),
]