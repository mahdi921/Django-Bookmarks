from django.urls import path
from image import views

app_name = "image"

urlpatterns = [
    path(
        "create/",
        views.ImageCreateView.as_view(),
        name="create"
    )
]
