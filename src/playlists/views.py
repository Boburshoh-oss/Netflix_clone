from django.utils import timezone
from django.http.response import Http404
from django.shortcuts import render
from .models import MovieProxy, PlayList, PublishStateOptions, TVShowProxy, TVShowSeasonProxy
from django.views import generic

# Create your views here.

class PlayListMixin():
    title = None
    template_name = 'playlist_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        if self.title is not None:
            context['title'] = self.title
        print(context)
        return context

    def get_queryset(self):
        return super().get_queryset().published()

class PlaylistDetailView(PlayListMixin,generic.DeleteView):
    template_name = 'playlists/playlist_detail.html'
    queryset = PlayList.objects.all()    
    title = 'Movies'

    # def get_object(self):
    #     kwargs = self.kwargs
    #     return self.get_queryset().filter(**kwargs).first()
        

class MovieListView(PlayListMixin,generic.ListView):
    queryset = MovieProxy.objects.all()    
    title = 'Movies'

class MovieDetailView(PlayListMixin,generic.DeleteView):
    template_name = 'playlists/movie_detail.html'
    queryset = MovieProxy.objects.all()    
    title = 'Movies'

class TVShowListView(PlayListMixin,generic.ListView):
    queryset = TVShowProxy.objects.all()
    title = 'TVShows'

class TVShowDetailView(PlayListMixin,generic.DeleteView):
    template_name = 'playlists/tvshow_detail.html'
    queryset = TVShowProxy.objects.all()    
    title = 'Movies'

class TVShowSeasonDetailView(PlayListMixin,generic.DeleteView):
    template_name = 'playlists/season_detail.html'
    queryset = TVShowSeasonProxy.objects.all()    
    title = 'Movies'

    def get_object(self):
        kwargs = self.kwargs
        show_slug = kwargs.get("showSlug")
        season_slug = kwargs.get("seasonSlug")
        now = timezone.now()
        try:
            obj = TVShowSeasonProxy.objects.get(
                state = PublishStateOptions.PUBLISH,
                publish_timestamp__lte=now,
                parent__slug__iexact=show_slug,
                slug__iexact=season_slug
            )
        except TVShowSeasonProxy.MultipleObjectsReturned:
            qs = TVShowSeasonProxy.objects.filter(
                parent__slug__iexact=show_slug,
                slug__iexact=season_slug
            ).published()
            obj = qs.first()
        except:
            raise Http404

        return obj
        # qs = self.get_queryset().filter(parent__slug__iexact=show_slug,slug__iexact=season_slug)
        # if not qs.count() == 1:
        #     raise Http404
        # return qs.first()

class FeaturedPlayListListView(PlayListMixin,generic.ListView):
    queryset = PlayList.objects.featured_playlist()
    title = 'Featured'
