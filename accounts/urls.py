from django.urls import path
from django.contrib.auth.views import ( \
    PasswordResetView, \
    PasswordResetConfirmView, \
    PasswordResetDoneView, \
    PasswordResetCompleteView)
from .views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path(
        'reset-password',
        PasswordResetView.as_view(template_name='password_reset.html'),
        name='reset_password'
    ),
    path(
        'reset-password-done',
        PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'reset-password/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(''
         'reset-password-complete',
         PasswordResetCompleteView.as_view(template_name='password_reset_complate.html'),
         name='password_reset_complete'
    ),
]
