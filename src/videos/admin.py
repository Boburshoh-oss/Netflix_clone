from django.contrib import admin
from .models import VideoAllProxy, VideoPublishedProxy, Video
# Register your models here.
class VideoAdmin(admin.ModelAdmin):
    list_display = ["title","video_id","state", "is_published"]
    search_fields = ['video_id']
    list_filter = ["active","state"]
    class Meta:
        model = Video
admin.site.register(Video,VideoAdmin)

class VideoAllAdmin(admin.ModelAdmin):
    list_display = ["title","video_id","state", "is_published"]
    search_fields = ['video_id']
    list_filter = ["active","state"]
    readonly_fields = ["id","is_published", "publish_timestamp","get_playlist_ids"]
    class Meta:
        model = VideoAllProxy
    
    # def published(self,obj):
    #     return obj.active

admin.site.register(VideoAllProxy, VideoAllAdmin)

class VideoPublishedProxyAdmin(admin.ModelAdmin):
    list_display = ["title","video_id"]
    search_fields = ['video_id']
    
    class Meta:
        model = VideoPublishedProxy
    
    def get_queryset(self, request):
        return VideoPublishedProxy.objects.filter(active=True)
        
admin.site.register(VideoPublishedProxy,VideoPublishedProxyAdmin)
