from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from . import api

urlpatterns = [
    # only register and login will be visible to all users
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user-login'),    
    # all other urls will require users to be logged in
    path('home/', login_required(login_url='../login/')(views.home), name='home'),
    path('logout/', login_required(login_url='../login/')(views.user_logout), name='logout'),
    path('profile/', login_required(login_url='../login/')(views.profile), name='profile'),
    path('search/', login_required(login_url='../login/')(views.search), name='search'),
    path('send_request/', login_required(login_url='../login/')(views.send_request), name='send-request'),
    path('remove_friend/', login_required(login_url='../login/')(views.remove_friend), name='remove-friend'),
    path('accept_request/', login_required(login_url='../login/')(views.accept_request), name='accept-request'),
    path('remove_request/', login_required(login_url='../login/')(views.remove_request), name='remove-request'),
    path('view/', login_required(login_url='../login/')(views.view), name='view-profile'),
    path('edit/', login_required(login_url='../login/')(views.edit), name='edit-profile'),
    path('api/user/<int:pk>', login_required(login_url='../../login/')(api.UserDetails.as_view()), name='user-api'),
]