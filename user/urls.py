from django.urls import path
from .views import Home, RegisterView, LoginView, LogoutView, ForgotPassword, PasswordResetSent, ResetPassword, profile
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path('home/', Home, name='home'),
    path('register/', RegisterView, name='register'),
     path('profile/', profile, name='profile'),
    path('', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),
    path('forgot-password/', ForgotPassword, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', PasswordResetSent, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', ResetPassword, name='reset-password'),
    path('colorpic/', include('colorpic.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)