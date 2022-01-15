from django.contrib import admin
from .models import PlayList, PlayListItem, PlayListTypeChoices, TVShowProxy, TVShowSeasonProxy, MovieProxy,PlayListRelated
from tags.admin import TaggedItemInline

class MovieProxyAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    # list_display = ['title','category']
    # field = ['title','decription','category','state',"video"]
    list_display = ['title','category','description','parent']
    fields = ["title","video",'category',"description","slug","state","active",'order']

    
    class Meta:
        model = MovieProxy
        
    def get_queryset(self, request):
        return MovieProxy.objects.all()
admin.site.register(MovieProxy,MovieProxyAdmin)

class SeasonEpisodeProxyInline(admin.TabularInline):
    model = PlayListItem
    extra = 0

class TVShowSeasonProxyAdmin(admin.ModelAdmin):
    inlines = [SeasonEpisodeProxyInline,TaggedItemInline]
    list_display = ['title','category','description','parent']
    fields = ['parent',"title","video",'category',"description","slug","state","active",'order']
    
    class Meta:
        model = TVShowSeasonProxy
    def get_queryset(self, request):
        return TVShowSeasonProxy.objects.all()
admin.site.register(TVShowSeasonProxy,TVShowSeasonProxyAdmin)

class TVShowSeasonProxyInline(admin.TabularInline):
    model = TVShowSeasonProxy
    extra = 0
    fields = ['order','title','state']

class TVShowProxyAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline,TVShowSeasonProxyInline]
    list_display = ['title','category','description','parent']
    fields = ["title","video","description","category","slug","state","active",'order']
    class Meta:
        model = TVShowProxy
    
    def get_queryset(self, request):
        return TVShowProxy.objects.all()
admin.site.register(TVShowProxy,TVShowProxyAdmin)

class PlayListRelatedInline(admin.TabularInline):
    model = PlayListRelated
    fk_name = 'playlist'
    extra = 0

class PlayListItemInline(admin.TabularInline):
    model = PlayListItem
    extra = 0
admin.site.register(PlayListItem)

class PlayListAdmin(admin.ModelAdmin):
    inlines = [PlayListItemInline,PlayListRelatedInline,TaggedItemInline]
    list_display = ['title','description','parent',"category"]
    fields = ["title","category","description","slug","state","active",'order']
    
    class Meta:
        model = PlayList
    
    def get_queryset(self, request):
        return PlayList.objects.filter(type=PlayListTypeChoices.PLAYLIST)
admin.site.register(PlayList,PlayListAdmin)

