from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.signIn, name='login'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('register/', views.signUp, name='register'),
    path('logout/', views.signOut, name='logout'),
    path('users-control/', views.usersControl, name='usersControl'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<uidb64>/<token>/', views.reset_password, name='reset_password'),

    path('notifications/delete/', views.delete_notifications, name='delete_notifications'),
    path('notifications/mark-as-read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),

    path('notifications/json/', views.get_notifications, name='notifications_json'),



]