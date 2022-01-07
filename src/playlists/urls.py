from django.urls import path
from .views import MovieListView, TVShowListView,FeaturedPlayListListView


urlpatterns = [
    path('movies/', MovieListView.as_view()),
    path('shows/', TVShowListView.as_view()),
    path('', FeaturedPlayListListView.as_view()),

]
