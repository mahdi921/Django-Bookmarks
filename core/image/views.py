from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from image.forms import ImageCreateForm


class ImageCreateView(LoginRequiredMixin, CreateView):
    '''Image creation view with authentication required'''
    form_class = ImageCreateForm
    template_name = "images/image/create.html"

    def get_initial(self):
        initial = super().get_initial()
        url = self.request.GET.get('url')
        if url:
            initial['url'] = url
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['preview_url'] = self.request.GET.get('url')
        return context

    def form_valid(self, form):
        # save instance, attach user profile,
        # show message and redirect to object URL
        new_image = form.save(commit=False)
        # ensure we assign a Profile instance, not the User
        try:
            profile = self.request.user.profile
        except AttributeError:
            from account.models import Profile
            profile = Profile.objects.get(user=self.request.user)
        new_image.user = profile
        new_image.save()
        messages.success(self.request, "Image added successfully.")
        return redirect(new_image.get_absolute_url())
