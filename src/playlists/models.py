from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from tags.models import TaggedItem
from ratings.models import Rating
from django.db.models import Avg, Max, Min, Q


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
    
    def search(self, query=None):
        if query is None:
            return self
        return self.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__title__icontains=query) |
            Q(category__slug__icontains=query) |
            Q(tags__tag__icontains=query) 
        ).movie_or_show().distinct()
    
    def movie_or_show(self):
        return self.filter(
            Q(type=PlayListTypeChoices.MOVIE) |
            Q(type=PlayListTypeChoices.SHOW)  
        )

class PlayListManager(models.Manager):
    def get_queryset(self):
        return PlayListQuerySet(self.model,using=self._db) 
    
    def published(self):
        return self.get_queryset().published()

    def featured_playlist(self):
        return self.get_queryset().filter(type=PlayListTypeChoices.PLAYLIST)
        
class PlayList(models.Model):
    parent = models.ForeignKey('self',on_delete=models.SET_NULL,null=True, blank=True)
    related = models.ManyToManyField('self', blank=True, related_name='related', through='PlayListRelated')
    category = models.ForeignKey("categories.Category", on_delete=models.SET_NULL,blank=True,null=True)
    order = models.IntegerField(default=1)
    category = models.ForeignKey("categories.Category",blank=True, null=True,on_delete=models.SET_NULL)
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
    tags = GenericRelation(TaggedItem, related_query_name='playlist')
    ratings = GenericRelation(Rating,related_query_name='playlist')

    objects = PlayListManager()
    
    # class Meta:
    #     unique_together = (('title','slug'))

    def __str__(self):
        return self.title
    
    def get_related_items(self):
        return self.playlistrelated_set.all()
    
    def get_absolute_url(self):
        if self.is_movie:
            return f"/playlist/movies/{self.slug}"
        if self.is_show:
            return f"/playlist/shows/{self.slug}"
        if self.is_season and self.parent is not None:
            return f"/playlist/shows/{self.parent.slug}/season/{self.slug}"
        return f"/playlists/{self.slug}"
        
    
    
    @property
    def is_season(self):
        return self.type == PlayListTypeChoices.SEASON
    
    @property
    def is_movie(self):
        return self.type == PlayListTypeChoices.MOVIE
    
    @property
    def is_show(self):
        return self.type == PlayListTypeChoices.SHOW

    def get_rating_avg(self):
        return PlayList.objects.filter(id=self.id).aggregate(Avg("ratings__value"))
    
    def get_rating_spread(self):
        return PlayList.objects.filter(id=self.id).aggregate(max=Max("ratings__value"), min=Min("ratings__value"))
    
    def save(self, *args, **kwargs):     
        if self.state == PublishStateOptions.PUBLISH and self.publish_timestamp is None:
            self.publish_timestamp = timezone.now()
        elif self.state == PublishStateOptions.DRAFT:
               self.publish_timestamp = None

        return super().save(*args,**kwargs)

    def get_short_display(self):
        return ""
    
    def get_video_id(self):
        """get main video id to render video for users"""
        if self.video is None:
            return None
        return self.video.get_video_id()

    def get_clips(self):
        """get clips id to render clips for users"""
        return self.playlistitem_set.all().published()

    @property
    def is_published(self):
        return self.active


class PlayListItemQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            playlist__state=PublishStateOptions.PUBLISH,
            playlist__publish_timestamp__lte = now,
            video__state=PublishStateOptions.PUBLISH,
            video__publish_timestamp__lte = now
        )

class PlayListItemManager(models.Manager):
    def get_queryset(self):
        return PlayListItemQuerySet(self.model,using=self._db) 
    
    def published(self):
        return self.get_queryset().published()

    def featured_playlist(self):
        return self.get_queryset().filter(type=PlayListTypeChoices.PLAYLIST)
    

class PlayListItem(models.Model):
    playlist = models.ForeignKey("playlists.PlayList", on_delete=models.CASCADE)
    video = models.ForeignKey("videos.Video", on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = PlayListItemManager()
    class Meta:
        ordering = ["order","-timestamp"]

class MovieProxyManager(PlayListManager):
    def all(self):
        return self.get_queryset().filter(type=PlayListTypeChoices.MOVIE)
    


class MovieProxy(PlayList):
    objects = MovieProxyManager()

    def get_movie_id(self):
        """get movie id to render movie for users"""
        
        return self.get_video_id()


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
    
    @property
    def seasons(self):
        return self.playlist_set.published()

    def get_short_display(self):
        return f"{self.seasons.count()} Seasons"

    def get_video_id(self):
        """get movie id to render movie for users"""
        if self.video is None:
            return None
        return self.video.get_video_id()

    def get_clips(self):
        """get clips id to render clips for users"""
        return self.playlistitem_set.all().published()

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
    
    def get_season_trailer(self):
        """get espisodes id to render  for users"""
        return self.get_video_id()
    
    def get_episodes(self):
        """get clips id to render clips for users"""
        qs = self.playlistitem_set.all().published()
        return qs

def pr_limit_choices_to():
    return Q(type=PlayListTypeChoices.MOVIE) | Q(type=PlayListTypeChoices.SHOW)

class PlayListRelated(models.Model):
    playlist = models.ForeignKey("playlists.PlayList", on_delete=models.CASCADE)
    related = models.ForeignKey("playlists.PlayList", on_delete=models.CASCADE, related_name='related_item', limit_choices_to=pr_limit_choices_to)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)