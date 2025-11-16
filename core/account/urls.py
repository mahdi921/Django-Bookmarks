from django.urls import path, reverse_lazy
from account import views
from django.contrib.auth import views as auth_views

app_name = "account"

urlpatterns = [
    # using django's built-in auth framework to handle authentication

    # login and logout urls
    path("login/", views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # change password urls
    path('password-change/',
         auth_views.PasswordChangeView.as_view(
             success_url=reverse_lazy('account:password_change_done')
         ),
         name='password_change'
         ),
    path(
        'password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(),
        name='password_change_done'
    ),

    # Reset password urls
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy('account:password_reset_done')
        ),
        name="password_reset"
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done"
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('account:password_reset_complete')
        ),
        name="password_reset_confirm"
    ),
    path(
        "password-reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete"
    ),

    # register user url
    path(
        'register/',
        views.RegistrationView.as_view(),
        name='register'
    ),

    # dashboard url
    path("", views.dashboard, name='dashboard'),
    path(
        'edit-profile/<int:pk>/',
        views.UpdateProfileView.as_view(),
        name="edit_profile"
    ),
    path(
        'edit-user/<int:pk>/',
        views.UpdateUserView.as_view(),
        name="edit_user"
    ),
]
