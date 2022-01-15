from django.http.response import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Count
from playlists.models import PlayList
# Create your views here.
from .models import Category


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

class CategoryListView(ListView):
    template_name = 'category_list.html'
    queryset = Category.objects.all().filter(active=True).annotate(pl_count=Count('playlist')).filter(pl_count__gt=0)
    
class CategoryDetailView(PlayListMixin,ListView):
    queryset = Category.objects.all().filter(active=True)
    
    def get_context_data(self):
        context = super().get_context_data()
        try:
            obj= Category.objects.get(slug=self.kwargs.get('slug'))
        except Category.DoesNotExist:
            raise Http404
        except Category.MultipleObjectsReturned:
            raise Http404
        except:
            obj = None
        context['object'] = obj
        
        if obj is not None:
            context['title'] = obj.title
        return context

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return PlayList.objects.filter(category__slug=slug).movie_or_show()
