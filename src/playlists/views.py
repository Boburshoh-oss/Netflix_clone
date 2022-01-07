from django.shortcuts import render
from .models import MovieProxy, PlayList, TVShowProxy
from django.views import generic
# Create your views here.

class PlayListMixin():
    title = None
    template_name = 'playlist_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        if self.title is not None:
            context['title'] = self.title
        return context

    def get_queryset(self):
        return super().get_queryset().published()

class MovieListView(PlayListMixin,generic.ListView):
    queryset = MovieProxy.objects.all()    
    title = 'Movies'

class TVShowListView(PlayListMixin,generic.ListView):
    queryset = TVShowProxy.objects.all()
    title = 'TVShows'

class FeaturedPlayListListView(PlayListMixin,generic.ListView):
    template_name = 'featured_list.html'
    queryset = PlayList.objects.featured_playlist()
    title = 'Featured'
