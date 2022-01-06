from django.contrib import admin
from .models import PlayList, PlayListItem, PlayListTypeChoices, TVShowProxy, TVShowSeasonProxy, MovieProxy
# Register your models here.


class MovieProxyAdmin(admin.ModelAdmin):
    list_display = ['title','parent']
    field = ['title','decription','category','state',"video","category"]

    
    class Meta:
        model = MovieProxy
        
    def get_queryset(self, request):
        return MovieProxy.objects.all()
admin.site.register(MovieProxy,MovieProxyAdmin)

class SeasonEpisodeProxyInline(admin.TabularInline):
    model = PlayListItem
    extra = 0

class TVShowSeasonProxyAdmin(admin.ModelAdmin):
    inlines = [SeasonEpisodeProxyInline]
    list_display = ['title','parent']
    field = ['title','decription','state',"video"]
    
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
    inlines = [TVShowSeasonProxyInline]
    field = ['title','decription','state',"video","category"]
    
    class Meta:
        model = TVShowProxy
    
    def get_queryset(self, request):
        return TVShowProxy.objects.all()
admin.site.register(TVShowProxy,TVShowProxyAdmin)


class PlayListItemInline(admin.TabularInline):
    model = PlayListItem
    extra = 0
admin.site.register(PlayListItem)

class PlayListAdmin(admin.ModelAdmin):
    inlines = [PlayListItemInline]
    list_display = ['title','description','parent']
    
    class Meta:
        model = PlayList
    
    def get_queryset(self, request):
        return PlayList.objects.filter(type=PlayListTypeChoices.PLAYLIST)
admin.site.register(PlayList,PlayListAdmin)

