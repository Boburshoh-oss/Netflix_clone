from django.urls import path, re_path
from .views import (MovieListView,
                    TVShowListView,
                    FeaturedPlayListListView,
                    MovieDetailView,
                    PlaylistDetailView,
                    TVShowDetailView,
                    TVShowSeasonDetailView,
                    SearchView
                    )


urlpatterns = [
    # re_path(r'my_detail/(?P<id>\d+)/$',FeaturedPlayListListView.as_view()),
    path('media/<int:pk>/', PlaylistDetailView.as_view()),
    path('movies/', MovieListView.as_view()),
    path('movies/<slug:slug>/', MovieDetailView.as_view()),
    path('shows/', TVShowListView.as_view()),
    path('shows/<slug:showSlug>/season/<slug:seasonSlug>/', TVShowSeasonDetailView.as_view()),
    path('shows/<slug:slug>/season/', TVShowListView.as_view()),
    path('shows/<slug:slug>/', TVShowDetailView.as_view()),
    path('', FeaturedPlayListListView.as_view()),
    path('search/', SearchView.as_view()),

]
