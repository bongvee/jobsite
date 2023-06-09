from django.urls import path
from . import views

urlpatterns = [
    path('signup-user/', views.signup_user, name='signup_user'),
    path('me/', views.currentUser, name='current_user'),
    # update user profile
    path('me/update/', views.updateUser, name='update_user'),
]