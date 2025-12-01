from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class ImageCreateView(LoginRequiredMixin, CreateView):
    '''Image creation view with authentication required'''
    from image.forms import ImageCreateForm
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
        from django.contrib import messages
        messages.success(self.request, "Image added successfully.")
        from django.shortcuts import redirect
        return redirect(new_image.get_absolute_url())


class ImageDetailView(DetailView):
    '''View to show image details'''
    from image.models import Image
    model = Image
    template_name = "images/image/detail.html"


class ImageLikeView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        image_id = request.POST.get("id")
        action = request.POST.get("action")

        from django.http import JsonResponse
        if action and image_id:
            try:
                from image.models import Image
                image = Image.objects.get(id=image_id)
                if action == "like":
                    image.users_like.add(request.user.profile)
                else:
                    image.users_like.remove(request.user.profile)
                return JsonResponse({"status": "ok"})
            except Image.DoesNotExist:
                pass
        return JsonResponse({"status": "error"})


class ImageListView(LoginRequiredMixin, ListView):
    from image.models import Image
    model = Image
    queryset = model.objects.all()
    paginate_by = 8
    context_object_name = "image"
    template_name = "images/image/list.html"

    def get_template_names(self):
        if self.request.GET.get("images_only"):
            return ["images/image/list_images.html"]
        return [self.template_name]

    def paginate_queryset(self, queryset, page_size):
        from django.core.paginator import (
            EmptyPage,
            PageNotAnInteger,
            Paginator
        )
        paginator = Paginator(queryset, page_size)
        page = self.request.GET.get('page')

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            if self.request.GET.get("images_only"):
                return paginator, [], None, None
            page_obj = paginator.page(paginator.num_pages)
        is_paginated = paginator.num_pages > 1
        return paginator, page_obj, page_obj.object_list, is_paginated

    def render_to_response(self, context, **response_kwargs):
        if not context["image"] and self.request.GET.get("images_only"):
            from django.http import HttpResponse
            return HttpResponse('')
        return super().render_to_response(context, **response_kwargs)
