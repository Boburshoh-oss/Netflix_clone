from django.http.response import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Count
from playlists.models import PlayList
from django.views import View
from .models import TaggedItem

class TaggedItemListView(View):
    def get(self,request):
        tag_list = TaggedItem.objects.unique_list()
        context = {
            'tag_list':tag_list
        }
        return render(request,'tags/tag_list.html',context)

class PlayListMixin():
    title = None
    template_name = 'playlist_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        if self.title is not None:
            context['title'] = self.title
        # print(context)
        return context

    def get_queryset(self):
        return super().get_queryset()
    
class TaggedItemDetailView(PlayListMixin,ListView):
    queryset = TaggedItem.objects.all()
    
    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = f"{self.kwargs.get('slug')}".title()
        return context

    def get_queryset(self):
        tag = self.kwargs.get('tag')
        return PlayList.objects.filter(tags__tag=tag).movie_or_show()
