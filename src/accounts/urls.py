from django.urls import path
from .views import Login, Logout, Account, ChangePassword, RegisterUser, ResetPassword
from django.contrib.auth import views as auth_views

app_name = 'account'
urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout')
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('', Account.as_view(), name='account'),
    path('change_password/', ChangePassword.as_view(), name='change'),
    path('reset_password/', ResetPassword.as_view(), name='reset')
]