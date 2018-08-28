from django.urls import path, include

from . import views
from django.contrib.auth import views as auth_views

from capapi.views import user_views
from capapi.forms import LoginForm


urlpatterns = [
    ### pages ###
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('tools/', views.tools, name='tools'),
    # path('showcase/', views.showcase, name='showcase'),


    ### user account pages ###

    # All templates live in capapi/registration for now
    path('login/', auth_views.LoginView.as_view(form_class=LoginForm), name='login'),


    path('register/', user_views.register_user, name='register'),
    path('verify-user/<int:user_id>/<activation_nonce>/', user_views.verify_user, name='verify-user'),
    # override default Django login view to use custom LoginForm
    path('accounts/', include('django.contrib.auth.urls')),  # logout, password change, password reset
    path('account/', user_views.user_details, name='user-details'),
    path('accounts/resend-verification/', user_views.resend_verification, name='resend-verification'),

]