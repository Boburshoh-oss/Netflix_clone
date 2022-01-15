from django.urls import path
from ratings.views import rate_object_view

urlpatterns = [
    path("object-rate/",rate_object_view)
]
