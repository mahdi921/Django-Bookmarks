# importing render to render
from django.shortcuts import render

# importing generic views
from django.views.generic import CreateView, UpdateView, ListView, DetailView

# importing django auth modules
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin

# importing reverse lazy for redirection
from django.urls import reverse_lazy

# importing custom forms
from account import forms
from account.models import Profile

# store user model to User
User = get_user_model()


class CustomLoginView(LoginView, AccessMixin):
    """
    using customized login view in order to deny access to authorized users
    """

    # denying access to authorized users
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class CustomLogoutView(LogoutView, AccessMixin):
    """
    custom logout view to tackle redirection to django's admin logout page
    """

    template_name = "registration/logout.html"


class RegistrationView(CreateView, AccessMixin):
    """
    registration view to sign up users using django's built-in form
    and a custom template
    """

    form_class = forms.UserRegistrationForm
    template_name = "account/register.html"
    success_url = reverse_lazy("account:login")

    # denying access to authorized users
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        message = "User account created successfully!"
        messages.success(self.request, message=message)
        return super().form_valid(form)

    def form_invalid(self, form):
        message = "Your input was incorrect.\
            please try again with correct info"
        messages.error(self.request, message=message)
        return super().form_invalid(form)


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """
    View to update user info
    """

    model = Profile
    form_class = forms.EditProfileForm
    success_url = reverse_lazy("account:dashboard")
    template_name = "account/profile_edit_form.html"

    def form_valid(self, form):
        message = "Profile updated successfully"
        messages.success(self.request, message=message)
        return super().form_valid(form)

    def form_invalid(self, form):
        message = "Your input was incorrect.\
            please try again with correct info"
        messages.error(self.request, message=message)
        return super().form_invalid(form)


class UpdateUserView(LoginRequiredMixin, UpdateView):
    """
    View to update user info
    """

    model = User
    form_class = forms.EditUserForm
    success_url = reverse_lazy("account:dashboard")
    template_name = "account/user_edit_form.html"

    def form_valid(self, form):
        message = "User info updated successfully"
        messages.success(self.request, message=message)
        return super().form_valid(form)

    def form_invalid(self, form):
        message = "Your input was incorrect.\
            please try again with correct info"
        messages.error(self.request, message=message)
        return super().form_invalid(form)


@login_required
def dashboard(request):
    """
    user dashboard view
    """
    return render(request, "account/dashboard.html", {"section": "dashboard"})


class UserListView(LoginRequiredMixin, ListView):
    model = Profile
    queryset = model.objects.filter(is_active=True)
    template_name = 'account/user/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section"] = "people"
        context["users"] = self.queryset
        return context


class UserDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'account/user/detail.html'
    context_object_name = "profile"

    def get_queryset(self):
        return self.model.objects.filter(user__is_active=True)
