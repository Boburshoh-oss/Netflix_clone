from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
class PublishStateOptions(models.TextChoices):
        PUBLISH = "PU", "Publish"
        DRAFT = 'DR', 'Draft'
        # UNLISTED = 'UN', 'Unlisted'
        # PRIVATE = 'PR', 'Private'

class PlayListTypeChoices(models.TextChoices):
    MOVIE = "MOV", "Movie"
    SHOW = 'TVS', 'TV Show'
    SEASON = 'SEA','Season'
    PLAYLIST = 'PLY','Playlist'

class PlayListQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte = now
        )

class PlayListManager(models.Manager):
    def get_queryset(self):
        return PlayListQuerySet(self.model,using=self._db) 
    
    def published(self):
        return self.get_queryset().published()
        
class PlayList(models.Model):
    parent = models.ForeignKey('self',on_delete=models.SET_NULL,null=True, blank=True)
    category = models.ForeignKey("categories.Category", on_delete=models.SET_NULL,blank=True,null=True)
    order = models.IntegerField(default=1)
    category = models.ForeignKey("categories.Category",blank=True, null=True,on_delete=models.SET_NULL,default=1)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=3,choices=PlayListTypeChoices.choices, default=PlayListTypeChoices.PLAYLIST)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video = models.ForeignKey("videos.Video", on_delete=models.SET_NULL, null=True, related_name="featured_playlist")
    videos = models.ManyToManyField('videos.Video',blank=True, related_name="playlist_item", through="PlayListItem")
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=2, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    
    objects = PlayListManager()
    
    def __str__(self):
        return self.title

   
    
    def save(self, *args, **kwargs):     
        if self.state == PublishStateOptions.PUBLISH and self.publish_timestamp is None:
            self.publish_timestamp = timezone.now()
        elif self.state == PublishStateOptions.DRAFT:
               self.publish_timestamp = None

        return super().save(*args,**kwargs)
    
    @property
    def is_published(self):
        return self.active
    

class PlayListItem(models.Model):
    playlist = models.ForeignKey("playlists.PlayList", on_delete=models.CASCADE)
    video = models.ForeignKey("videos.Video", on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["order","-timestamp"]

class MovieProxyManager(PlayListManager):
    def all(self):
        return self.get_queryset().filter(type=PlayListTypeChoices.MOVIE)

class MovieProxy(PlayList):
    objects = MovieProxyManager()
    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        proxy = True  
    
    def save(self, *args, **kwargs):
        self.type = PlayListTypeChoices.MOVIE
        return super().save(*args, **kwargs)

class TVShowProxyManager(PlayListManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=True,type=PlayListTypeChoices.SHOW)

class TVShowProxy(PlayList):
    objects = TVShowProxyManager()
    class Meta:
        verbose_name = "TV Show"
        verbose_name_plural = "TV Shows"
        proxy = True  
    
    def save(self, *args, **kwargs):
        self.type = PlayListTypeChoices.SHOW
        return super().save(*args, **kwargs)

class TVShowSeasonProxyManager(PlayListManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=False,type=PlayListTypeChoices.SEASON)

class TVShowSeasonProxy(PlayList):
    objects = TVShowSeasonProxyManager()
    class Meta:
        verbose_name = "Season"
        verbose_name_plural = "Seasons"
        proxy = True

    def save(self, *args, **kwargs):
        self.type = PlayListTypeChoices.SEASON
        return super().save(*args, **kwargs)

